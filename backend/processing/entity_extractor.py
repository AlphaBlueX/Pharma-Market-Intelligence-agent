import re
from typing import List, Dict

# Simple rule-based entity extraction for pharma
DRUGS = ["Humira", "Keytruda", "Revlimid", "Eliquis", "Opdivo", "Imbruvica", "Stelara", "Eylea", "Xarelto", "Biktarvy"]
BRANDS = ["Pfizer", "Roche", "AbbVie", "Johnson & Johnson", "Merck", "Novartis", "AstraZeneca", "Sanofi", "Bristol Myers Squibb", "GSK"]
DISEASES = ["Cancer", "Diabetes", "Psoriasis", "Arthritis", "HIV", "Leukemia", "Lymphoma", "Melanoma", "COVID-19", "Alzheimer's"]

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extracts simple pharma-related entities using keyword matching.
    """
    found_entities = {
        "drugs": [],
        "brands": [],
        "diseases": []
    }
    
    text_lower = text.lower()
    
    for drug in DRUGS:
        if drug.lower() in text_lower:
            found_entities["drugs"].append(drug)
            
    for brand in BRANDS:
        if brand.lower() in text_lower:
            found_entities["brands"].append(brand)
            
    for disease in DISEASES:
        if disease.lower() in text_lower:
            found_entities["diseases"].append(disease)
            
    return found_entities
