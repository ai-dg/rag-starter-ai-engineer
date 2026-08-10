import os
import glob

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

DOCS_DIR = "docs"
CHUNK_SIZE = 500
TOP_K = 3
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = "Tu es un assistant qui repond aux questions des apprenants sur les contenus de formation. Reponds en francais."

app = FastAPI(title="Formation Assistant RAG")

vectorstore = None
llm = None


class Question(BaseModel):
    question: str


def load_docs():
    print("chargement des documents...")
    texts = []
    files = glob.glob(DOCS_DIR + "/*.md")
    for f in files:
        content = open(f).read()
        texts.append(content)
        print("ok ->", f)
    print(f"{len(texts)} fichiers charges")
    return texts


def chunk_text(text):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + CHUNK_SIZE])
        i = i + CHUNK_SIZE
    return chunks


def build_index():
    texts = load_docs()

    all_chunks = []
    for t in texts:
        for c in chunk_text(t):
            all_chunks.append(c)

    print(f"{len(all_chunks)} chunks generes")

    docs = []
    for c in all_chunks:
        docs.append(Document(page_content=c))

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    store = Chroma.from_documents(docs, embeddings)

    print("index construit")
    return store


def retrieve(question):
    results = vectorstore.similarity_search(question, k=TOP_K)
    context = ""
    for r in results:
        context = context + r.page_content + "\n\n"
    return context


def generate(question, context):
    prompt = f"""{SYSTEM_PROMPT}

Contexte :
{context}

Question : {question}

Reponse :"""

    response = llm.invoke(prompt)
    return response.content


@app.on_event("startup")
def startup():
    global vectorstore, llm
    print("demarrage du serveur")
    vectorstore = build_index()
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    print("serveur pret")


@app.post("/ask")
def ask(q: Question):
    print("question recue :", q.question)
    context = retrieve(q.question)
    answer = generate(q.question, context)
    print("reponse generee")
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
