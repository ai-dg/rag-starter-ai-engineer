"""
API routes.

This module is the entry point of the RAG system. It receives HTTP requests,
validates their data, coordinates the retrieval and generation pipelines, and
returns structured HTTP responses.

Responsibilities:
- Expose the API endpoints, such as `POST /query` and `GET /health`.
- Validate incoming request data.
- Call the retrieval pipeline to find relevant document chunks.
- Return a controlled "I don't know" response when no relevant context is found.
- Call the generation pipeline when sufficient context is available.
- Build structured JSON responses containing the answer and its sources.
- Handle application errors and return appropriate HTTP status codes.

Main endpoints:
- `POST /query`: receive a user's question and return a grounded answer.
- `GET /health`: report whether the API is running and ready to receive requests.

Request flow:
    HTTP request
        -> request validation
        -> document retrieval
        -> relevance guardrail
        -> answer generation
        -> JSON response

Important:
The API coordinates the different components but should not contain the internal
logic for document ingestion, vector search, or prompt construction.
"""

from fastapi import APIRouter

from app.schemas import HealthAnswer, QueryAnswer, QueryQuestion

router = APIRouter()


@router.get("/health", response_model=HealthAnswer)
def health() -> HealthAnswer:
    return HealthAnswer(status="ok")


@router.post("/query", response_model=QueryAnswer)
def query(payload: QueryQuestion) -> QueryAnswer:
    return QueryAnswer(
        answer="Not implemented yet",
        context_found=False,
    )




# @app.post("/ask")
# def ask(q: Question):
#     print("question recue :", q.question)
#     context = retrieve(q.question)
#     answer = generate(q.question, context)
#     print("reponse generee")
#     return {"answer": answer}

