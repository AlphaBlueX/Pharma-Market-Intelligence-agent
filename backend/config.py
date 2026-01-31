import os
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    HF_MODEL_ID = os.getenv("HF_MODEL_ID", "FlashLabs/Chroma-4B")
    
    # Fail fast if essential reasoning engine key is missing
    if not GEMINI_API_KEY and not HF_TOKEN:
        raise ValueError("FATAL: Both GEMINI_API_KEY and HF_TOKEN are missing. Please set at least one in the .env file.")
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DATA_DIR = os.getenv("DATA_DIR", "data")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vectors/faiss_index")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Variables for ingestion control
    INGEST_INTERVAL_HOURS = int(os.getenv("INGEST_INTERVAL_HOURS", 12))
    DOMAIN_RESTRICTION = os.getenv("DOMAIN_RESTRICTION", "pharma")
    LAST_INGEST_FILE = os.path.join(DATA_DIR, "last_ingest.txt")

    @classmethod
    def validate(cls):
        pass

config = Config()
