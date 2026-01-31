import requests
import json
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

dummy_data = [
    {
        "title": "AstraZeneca Vaccine Update",
        "text": "AstraZeneca reports high efficacy for its new vaccine variant. Trials show 95% protection against emerging strains.",
        "source": "Health News",
        "date": datetime.now().isoformat()
    },
    {
        "title": "Moderna Oncology Breakthrough",
        "text": "Moderna announces a new mRNA therapy for skin cancer. This is a game changer for the biotech industry.",
        "source": "Science Daily",
        "date": datetime.now().isoformat()
    }
]

def test_ingest():
    print("Testing forced ingestion...")
    resp = requests.post(f"{BACKEND_URL}/ingest/news?force=true", json=dummy_data)
    print(f"Status: {resp.status_code}")
    print(resp.json())

def test_alerts():
    print("\nTesting alerts retrieval...")
    resp = requests.get(f"{BACKEND_URL}/query/alerts")
    print(f"Status: {resp.status_code}")
    print(f"Alerts found: {len(resp.json())}")

def test_trends():
    print("\nTesting trends retrieval...")
    resp = requests.get(f"{BACKEND_URL}/query/trends")
    print(f"Status: {resp.status_code}")
    print(resp.json())

if __name__ == "__main__":
    test_ingest()
    test_alerts()
    test_trends()
