from fastapi import Depends, FastAPI
from app.api.routes import router
from app.core.auth import require_api_key
from app.llm.ollama_client import OllamaClient
from app.core.config import get_settings

app = FastAPI(
    title="Private Domain AI API",
    description="Local-first AI assistant for Purchasing, Logistics, Sourcing, and Warehouse.",
    version="0.1.0",
)

settings = get_settings()
ollama = OllamaClient(settings.ollama_base_url, settings.request_timeout_seconds)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "private-domain-ai"}


@app.get("/health/llm", dependencies=[Depends(require_api_key)])
async def llm_health() -> dict:
    available = await ollama.is_available()
    return {"ollama_available": available}

app.include_router(router)
