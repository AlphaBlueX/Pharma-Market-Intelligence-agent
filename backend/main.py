from fastapi import FastAPI
from backend.api import ingest_api, query_api
from backend.config import config

app = FastAPI(title="Pharma Market Intelligence Agent API")

# Include routers
app.include_router(ingest_api.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query_api.router, prefix="/query", tags=["Query"])

@app.get("/")
async def root():
    return {"message": "Pharma Market Intelligence Agent is online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
