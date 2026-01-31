import os
import json
import glob
from typing import List, Dict, Any
from backend.config import config

# Critical keywords for detecting valid drug launches/approvals
VALID_DRUG_KEYWORDS = [
    "FDA approval", "approved by FDA", "drug launch", 
    "Phase III", "clinical trial", "new treatment", 
    "breakthrough therapy", "marketing authorization"
]

# Keywords to exclude (stock market/financial fluff)
EXCLUDE_KEYWORDS = ["IPO", "stock listing", "earnings", "acquisition", "shares", "dividend"]

def retrieve_context(query: str, k: int = 5) -> str:
    """
    Retrieves the most relevant grounded documents from data/incoming/ files.
    Strictly filters for pharmaceutical relevance and excludes stock-related news.
    """
    incoming_dir = os.path.join(config.DATA_DIR, "incoming")
    files = glob.glob(os.path.join(incoming_dir, "ingest_*.json"))
    
    query_terms = query.lower().split()
    matched_articles = []

    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            title = data.get("title", "")
            content = data.get("content", "")
            text_to_check = (title + " " + content).lower()
            
            # 1. Domain Match: Must contain at least one query term
            if not any(term in text_to_check for term in query_terms):
                continue
                
            # 2. Validity Check: Must contain drug launch/approval keywords
            has_valid_keyword = any(kw.lower() in text_to_check for kw in VALID_DRUG_KEYWORDS)
            if not has_valid_keyword:
                continue
                
            # 3. Exclusion Check: Must NOT contain stock/financial fluff
            has_exclude_keyword = any(kw.lower() in text_to_check for kw in EXCLUDE_KEYWORDS)
            if has_exclude_keyword:
                continue
            
            matched_articles.append({
                "title": title,
                "source": data.get("source", "Unknown"),
                "date": data.get("published_at", "Unknown Date"),
                "content": content
            })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if not matched_articles:
        return ""

    # Sort by date (newest first) and take top k
    matched_articles.sort(key=lambda x: x['date'], reverse=True)
    top_articles = matched_articles[:k]
    
    context = ""
    for art in top_articles:
        context += f"Source: {art['source']}, {art['date']}\n"
        context += f"Title: {art['title']}\n"
        context += f"Content: {art['content']}\n\n"
    
    return context.strip()
