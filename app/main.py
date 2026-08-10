"""
FastAPI application entry point.

This module creates the application and registers its API routes.
"""

from fastapi import FastAPI
from app.api.routes import router
from app.config import Settings

settings = Settings()

app = FastAPI(title="Formation Assistant RAG")

app.include_router(router)



# @app.on_event("startup")
# def startup():
#     global vectorstore, llm
#     print("demarrage du serveur")
#     vectorstore = build_index()
#     llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
#     print("serveur pret")