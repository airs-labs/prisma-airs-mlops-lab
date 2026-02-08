"""FastAPI server for Cloud Security Advisor.

Serves a chat interface backed by a fine-tuned LLM via Vertex AI
or local model inference.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from airs_mlops_lab.serving.inference_client import get_inference_client

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize inference client on startup."""
    client = get_inference_client()
    health = await client.health_check()
    print(f"Inference backend: {health}")
    yield


app = FastAPI(
    title="AIRS MLOps Lab - Cloud Security Advisor",
    description="AI-powered cloud security guidance with AIRS model scanning",
    version="0.2.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str
    history: list[dict[str, str]] | None = None
    max_tokens: int = 512
    temperature: float = 0.7


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""

    reply: str


class HealthResponse(BaseModel):
    """Response body for health endpoint."""

    status: str
    backend: str
    version: str = "0.2.0"


@app.get("/", include_in_schema=False)
async def root():
    """Serve the chat UI."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/compare", include_in_schema=False)
async def compare():
    """A/B testing comparison UI."""
    return FileResponse(STATIC_DIR / "compare.html")


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    client = get_inference_client()
    info = await client.health_check()
    return HealthResponse(
        status=info.get("status", "unknown"),
        backend=info.get("backend", "unknown"),
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint for the security advisor.

    Sends the user message to the configured LLM backend
    and returns the generated response.
    """
    client = get_inference_client()
    reply = await client.chat(
        message=request.message,
        history=request.history,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    return ChatResponse(reply=reply)
