"""
FastAPI application entry point.

This module creates the application and registers its API routes.
"""

from fastapi import FastAPI
from app.api.routes import router
from app.config import Settings
from app.logger import configure_logging

settings = Settings()
configure_logging()

app = FastAPI(title="Formation Assistant RAG")

app.include_router(router)
