"""
Document retrieval pipeline.

This module searches the vector store for the chunks that are most relevant to
the user's question. It also applies a relevance-based guardrail before the
chunks are sent to the generation pipeline.

Responsibilities:
- Receive the user's question.
- Generate an embedding for the question.
- Search Chroma for the nearest document vectors.
- Retrieve the most relevant chunks, together with their scores and metadata.
- Compare the best retrieval score with a configurable relevance threshold.
- Reject the retrieved context when no result is found or when its relevance
  score is below the threshold.

Input:
- The user's question.

Output:
- The relevant chunks, scores, and metadata when sufficient context is found.
- An empty result when the available documents are not relevant enough.

Guardrail:
The generation pipeline should only be called when the retrieval result passes
the relevance threshold. Otherwise, the API returns a controlled "I don't know"
response without calling the LLM.

Important:
Depending on the Chroma method used, the returned value may be a relevance
score, where a higher value is better, or a distance, where a lower value is
better. The threshold comparison must follow the returned score type.
"""


# def retrieve(question):
#     results = vectorstore.similarity_search(question, k=TOP_K)
#     context = ""
#     for r in results:
#         context = context + r.page_content + "\n\n"
#     return context

