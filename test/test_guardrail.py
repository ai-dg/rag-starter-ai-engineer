from unittest.mock import patch

from langchain_core.documents import Document

from app.services.retrieval import retrieve


def test_guardrail_rejects_low_relevance_score():
    fake_doc = Document(page_content="hors sujet", metadata={"source": "x.md"})

    with patch("app.services.retrieval.vector_store") as mock_store:
        mock_store.similarity_search_with_score.return_value = [(fake_doc, 1.5)]
        result = retrieve("question hors sujet")

    assert result["context_found"] is False
    assert result["chunks"] == []


def test_guardrail_accepts_high_relevance_score():
    fake_doc = Document(page_content="dans le sujet", metadata={"source": "x.md"})

    with patch("app.services.retrieval.vector_store") as mock_store:
        mock_store.similarity_search_with_score.return_value = [(fake_doc, 0.3)]
        result = retrieve("question dans le sujet")

    assert result["context_found"] is True
    assert len(result["chunks"]) == 1