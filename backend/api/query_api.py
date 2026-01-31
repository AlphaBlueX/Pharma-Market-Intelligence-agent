from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.agent.insight_engine import insight_engine
from backend.config import config
from backend.vectorstore.vectordb import vectordb
import os
import json

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    insight: str

# Expanded Pharma keywords for domain restriction
PHARMA_KEYWORDS = [
    "drug", "pharma", "medicine", "clinical", "trial", "diagnosis", "disease", "therapy", 
    "fda", "hospital", "patient", "paracetamol", "aspirin", "ibuprofen", "vaccine", "vacine",
    "oncology", "diabetes", "cardiac", "statin", "insulin", "biotech", "treatment",
    "medication", "pharmacy", "doctor", "health", "care", "wellness", "prescription",
    "med", "pill", "tablet", "capsule", "injection", "dose", "covid", "corona", "virus"
]

def is_pharma_related(text: str) -> bool:
    text_lower = text.lower().strip()
    # Allow common greetings so the bot can say hi back
    greetings = ["hi", "hello", "hey", "help", "who are you"]
    if text_lower in greetings:
        return True
    
    return any(keyword in text_lower for keyword in PHARMA_KEYWORDS)

@router.post("/", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Queries the AI agent for market insights based on RAG.
    Includes domain restriction check.
    """
    if not is_pharma_related(request.query):
        return QueryResponse(insight="I don't know your details. I am a specialized Pharma Market Intelligence Agent. Please ask me questions related to drugs, clinical trials, or pharmaceutical market trends.")

    try:
        insight = insight_engine.generate_insight(request.query)
        return QueryResponse(insight=insight)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def status():
    return {"status": "ready"}

@router.get("/alerts")
async def get_alerts():
    """Retrieves persisted market alerts."""
    alerts_file = os.path.join(config.DATA_DIR, "alerts.json")
    if os.path.exists(alerts_file):
        with open(alerts_file, "r") as f:
            return json.load(f)
    return []

@router.get("/trends")
async def get_trends():
    """Retrieves trend data based on brand mentions in the vector store."""
    metadata = vectordb.metadata
    brand_counts = {}
    
    # Simple logic: count mentions of common pharma brands
    BRANDS = ["Pfizer", "Roche", "Novartis", "Merck", "Moderna", "AstraZeneca", "PharmaCorp"]
    
    for m in metadata:
        text = m.get("text", "").lower()
        for brand in BRANDS:
            if brand.lower() in text:
                brand_counts[brand] = brand_counts.get(brand, 0) + 1
                
    return {
        "brand_mentions": brand_counts,
        "total_documents": len(metadata)
    }
