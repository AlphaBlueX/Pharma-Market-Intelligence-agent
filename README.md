# Pharma Market Intelligence Agent

## Problem Statement
Pharmaceutical companies operate in a fast-paced environment where market dynamics, regulatory changes, and competitive maneuvers happen daily. Staying ahead requires continuous monitoring of vast amounts of data. Most existing solutions are either manual or rely on generic AI that lacks long-term context (memory) and pharmaceutical specialization.

## Architecture
This project implements an **Always-On RAG-based AI Agent** designed specifically for pharma market intelligence.

1.  **Ingestion (n8n)**: Orchestrates data fetching from news APIs or brand communications and pushes it to the backend.
2.  **FastAPI Backend**:
    *   **Processing**: Cleans text, extracts pharma-specific entities (drugs, brands, diseases), and performs sentiment analysis.
    *   **Domain Safety**: Strictly filters incoming data and user queries for pharmaceutical relevance.
    *   **Memory (FAISS)**: Stores processed data as semantic embeddings. Implements **Smart Retention** where old data is summarized into "long-term memory" every 12 hours.
    *   **Reasoning Engine**: Uses **Hugging Face (FlashLabs/Chroma-4B)** or Google Gemini for strategic analysis over retrieved context.
3.  **UI (Streamlit)**: A multi-page dashboard for interactive intelligence analysis.

## Hackathon Pitch
"Meet the Pharma Market Intelligence Agent—your AI-driven strategic partner. Built for discipline and production-readiness, our agent features a 12-hour ingestion throttle, hard domain filtering to prevent 'off-topic' queries, and a smart memory pruning system. Now upgraded with local LLM capabilities via Hugging Face for enhanced private reasoning."

## How to Run

### 1. Prerequisites
*   Python 3.9+
*   Hugging Face Token (for `FlashLabs/Chroma-4B`)
*   Gemini API Key (Optional fallback)
*   FAISS and other dependencies (`pip install -r requirements.txt`)

### 2. Setup Environment
Create a `.env` file in the project root with the following:
```env
HF_TOKEN=your_hf_token_here
HF_MODEL_ID=FlashLabs/Chroma-4B
GEMINI_API_KEY=optional_fallback_key
INGEST_INTERVAL_HOURS=12
DOMAIN_RESTRICTION=pharma
```

### 3. Start Backend
```bash
uvicorn backend.main:app --reload
```

### 4. Start UI
```bash
streamlit run ui.app
```

## UI Structure
The system uses a multi-page Streamlit layout:
- **Landing Page**: Overview and configuration.
- **Dashboard**: Strategic querying and insight generation.
- **Alerts**: Real-time monitoring log.
- **Trends**: Brand sentiment visualization.

## Key Production Features
- **Hugging Face Integration**: Powered by `FlashLabs/Chroma-4B` for high-quality local reasoning.
- **12-Hour Ingestion Rule**: Prevents redundant processing and manages API usage.
- **Pharma Domain Restriction**: Hard-filters both data and queries for industry relevance.
- **Smart Data Retention**: Summarizes historical data, keeping the memory footprint efficient.
