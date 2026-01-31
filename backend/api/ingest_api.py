from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import os
import time
import json
from datetime import datetime, timedelta
import google.generativeai as genai

from backend.processing.cleaner import clean_text
from backend.processing.entity_extractor import extract_entities
from backend.embeddings.embedder import embedder
from backend.vectorstore.vectordb import vectordb
from backend.agent.alert_engine import alert_engine
from backend.config import config
from backend.rag.prompts import PHARMA_SUMMARY_PROMPT

router = APIRouter()

@router.post("")
async def receive_ingest(request: Request):
    """
    Receives raw JSON from n8n, logs it, and saves it to data/incoming/.
    This endpoint is more resilient to schema changes.
    """
    try:
        body = await request.json()
        print(f"[{datetime.now().isoformat()}] Received ingest request from {request.client.host}")
        
        # Ensure data/incoming directory exists
        incoming_dir = os.path.join(config.DATA_DIR, "incoming")
        os.makedirs(incoming_dir, exist_ok=True)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ingest_{timestamp}.json"
        filepath = os.path.join(incoming_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(body, f, indent=4)
            
        print(f"[{datetime.now().isoformat()}] Saved ingestion to {filepath}")
        
        return {"status": "success", "message": "Data received and stored", "file": filename}
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] Error in /ingest: {str(e)}")
        return {"status": "error", "message": str(e)}

class NewsItem(BaseModel):
    title: str
    text: str
    source: Optional[str] = "Web"
    date: Optional[str] = None

# Task 3: Domain keywords - expanded for realism
PHARMA_KEYWORDS = [
    "drug", "pharma", "medicine", "clinical", "trial", "diagnosis", "disease", "therapy", 
    "fda", "hospital", "patient", "paracetamol", "aspirin", "ibuprofen", "vaccine", "vacine",
    "oncology", "diabetes", "cardiac", "statin", "insulin", "biotech", "treatment",
    "medication", "pharmacy", "doctor", "health", "care", "wellness", "prescription",
    "med", "pill", "tablet", "capsule", "injection", "dose", "covid", "corona", "virus"
]

def is_pharma_related(text: str) -> bool:
    text_lower = text.lower().strip()
    return any(keyword in text_lower for keyword in PHARMA_KEYWORDS)

@router.post("/news")
async def ingest_news(items: List[NewsItem], force: bool = False):
    """
    Ingests news items from n8n with:
    - 12-hour interval check (bypassable with force=True)
    - Pharma domain restriction
    - Smart data retention (old data summarization)
    """
    
    # Task 4: Ingestion Rate Limit (12-Hour Rule)
    now = datetime.now()
    if not force and os.path.exists(config.LAST_INGEST_FILE):
        with open(config.LAST_INGEST_FILE, "r") as f:
            last_ingest_str = f.read().strip()
            if last_ingest_str:
                last_ingest_time = datetime.fromisoformat(last_ingest_str)
                if now - last_ingest_time < timedelta(hours=config.INGEST_INTERVAL_HOURS):
                    return {"status": "skipped", "message": "Ingestion skipped – interval not reached. Use force=True to bypass."}

    # Task 5: Smart Data Retention (Pruning & Summarization)
    # 1. Summarize old data before clearing
    old_metadata = vectordb.metadata
    if old_metadata:
        try:
            # Extract just titles and entities for the summarizer to keep it concise
            summary_source = "\n".join([f"Title: {m.get('title')}, Entities: {m.get('entities')}" for m in old_metadata])
            prompt = PHARMA_SUMMARY_PROMPT.format(old_data=summary_source[:2000]) # Limit input

            summary_text = ""
            # Check if we should use HF or Gemini
            if config.HF_TOKEN:
                # Use shared InsightEngine model/processor if possible, or local load
                # For simplicity in this demo, we'll try to use the insight_engine's model
                from backend.agent.insight_engine import insight_engine
                if insight_engine.use_hf and insight_engine._model:
                    inputs = insight_engine._tokenizer(prompt, return_tensors="pt").to(insight_engine._model.device)
                    outputs = insight_engine._model.generate(**inputs, max_new_tokens=300)
                    input_len = inputs["input_ids"].shape[1]
                    summary_text = insight_engine._tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
            
            if not summary_text and config.GEMINI_API_KEY:
                genai.configure(api_key=config.GEMINI_API_KEY)
                model = genai.GenerativeModel(config.MODEL_NAME)
                response = model.generate_content(prompt)
                summary_text = response.text
            
            if not summary_text:
                summary_text = "Key drugs and diagnoses observed so far: [Data cleared, summarization skipped]"

            # 2. Clear old data (Re-initialize vector DB)
            import faiss
            vectordb.index = faiss.IndexFlatL2(vectordb.dimension)
            vectordb.metadata = []
            
            # 3. Store summary in Vector DB
            summary_vector = embedder.get_embeddings(summary_text)
            vectordb.add_document(summary_vector, {
                "title": "Historical Market Summary",
                "text": summary_text,
                "source": "System Memory",
                "date": now.isoformat(),
                "entities": {"summary": True}
            })
        except Exception as e:
            print(f"Error during pruning/summarization: {e}")

    processed_count = 0
    alerts = []
    
    for item in items:
        # Task 3: Domain Restriction
        if not is_pharma_related(item.text):
            continue

        # 1. Clean Text
        cleaned_text = clean_text(item.text)
        
        # 2. Extract Entities
        entities = extract_entities(cleaned_text)
        
        # 3. Generate Embedding
        vector = embedder.get_embeddings(cleaned_text)
        
        # 4. Store in Vector DB
        metadata = {
            "title": item.title,
            "text": cleaned_text,
            "source": item.source,
            "date": item.date,
            "entities": entities
        }
        vectordb.add_document(vector, metadata)
        
        # 5. Check for alerts
        alert_info = alert_engine.process_news(metadata)
        if alert_info["is_alert"]:
            alerts.append(alert_info)
            
        processed_count += 1
    
    # Update last ingest time
    with open(config.LAST_INGEST_FILE, "w") as f:
        f.write(now.isoformat())
        
    # Persist alerts to file
    if alerts:
        alerts_file = os.path.join(config.DATA_DIR, "alerts.json")
        existing_alerts = []
        if os.path.exists(alerts_file):
            import json
            try:
                with open(alerts_file, "r") as f:
                    existing_alerts = json.load(f)
            except:
                pass
        
        # Keep only last 50 alerts
        all_alerts = alerts + existing_alerts
        with open(alerts_file, "w") as f:
            import json
            json.dump(all_alerts[:50], f, indent=4)
            
    return {
        "status": "success",
        "processed_count": processed_count,
        "alerts_generated": len(alerts),
        "alerts": alerts
    }
