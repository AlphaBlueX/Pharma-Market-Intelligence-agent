import requests
import json
from datetime import datetime
import time

BACKEND_URL = "http://localhost:8000"

dummy_data = [
    {
        "title": "FDA Approves New Psoriasis Drug",
        "text": "The FDA has granted approval for Dermacure, a breakthrough therapy for plaque psoriasis. Clinical trials showed 90% clearance in patients within 12 weeks. This is a significant win for PharmaCorp.",
        "source": "PharmaNews Daily",
        "date": datetime.now().isoformat()
    },
    {
        "title": "Roche Expands Oncology Portfolio",
        "text": "Roche announced today that it is acquiring a small biotech firm to bolster its oncology pipeline. The deal focuses on innovative cancer treatments for lymphoma and melanoma.",
        "source": "MarketWatch",
        "date": datetime.now().isoformat()
    },
    {
        "title": "Statin Usage Trends in 2026",
        "text": "Recent data suggests a 15% increase in statin prescriptions globally. Doctors are focusing on cardiac wellness and preventative medicine for aging populations.",
        "source": "Health Trends Report",
        "date": datetime.now().isoformat()
    },
    {
        "title": "Aspirin and Paracetamol Supply Chain Update",
        "text": "Global supply chains for common medications like aspirin and paracetamol are stabilizing. Manufacturers in India and China report increased production capacity for essential pain relief drugs.",
        "source": "Reuters Pharma",
        "date": datetime.now().isoformat()
    },
    {
        "title": "New Vaccine for Seasonal Flu Enters Phase III",
        "text": "A novel mRNA-based vaccine for seasonal influenza has entered Phase III clinical trials. Initial results indicate strong immune responses with minimal side effects.",
        "source": "Biotech Insider",
        "date": datetime.now().isoformat()
    }
]

def ingest_with_retry(retries=30, delay=5):
    print(f"Waiting for backend at {BACKEND_URL}...")
    for i in range(retries):
        try:
            health = requests.get(f"{BACKEND_URL}/")
            if health.status_code == 200:
                print("Backend is online! Ingesting data...")
                response = requests.post(f"{BACKEND_URL}/ingest/news?force=true", json=dummy_data)
                if response.status_code == 200:
                    print("Ingestion Success!")
                    print(json.dumps(response.json(), indent=2))
                    return True
                else:
                    print(f"Ingestion Error: {response.status_code}")
            else:
                print(f"Backend status: {health.status_code}")
        except Exception as e:
            print(f"Attempt {i+1}/{retries}: Backend not ready yet...")
        time.sleep(delay)
    return False

if __name__ == "__main__":
    ingest_with_retry()
