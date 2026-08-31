"""
FastAPI app ka entry point. Abhi sirf health-check route hai.
Agle stages mein yahan routing/chat routes add karenge.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat import router as chat_router

app = FastAPI(title="LLM Cost Autopilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}
