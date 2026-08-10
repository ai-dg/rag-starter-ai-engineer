"""
Answer generation pipeline.

This module uses a Large Language Model (LLM) to generate an answer from the
user's question and the chunks selected by the retrieval pipeline.

Responsibilities:
- Build the prompt sent to the LLM.
- Add the retrieved chunks as context.
- Instruct the model to answer only from the provided context.
- Generate a clear and relevant final answer.
- Associate the answer with its document sources.
- Return a controlled "I don't know" response when the context does not
  contain enough information.

Inputs:
- The user's question.
- The relevant chunks returned by the retrieval pipeline.

Output:
- A generated answer grounded in the retrieved documents.
"""



# def generate(question, context):
#     prompt = f"""{SYSTEM_PROMPT}

# Contexte :
# {context}

# Question : {question}

# Reponse :"""

#     response = llm.invoke(prompt)
#     return response.content


