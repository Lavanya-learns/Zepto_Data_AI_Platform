from pathlib import Path
import os

from sentence_transformers import SentenceTransformer
import chromadb
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from fastapi import FastAPI


MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"


def build_prompt(query, context):
    return f"""
Role:
You are a Zepto customer support assistant.

Context:
Use only the retrieved Zepto policy information below.
{context}

Task:
Answer the user's question using only the provided context.

Format:
Give a clear and direct answer. Do not make up information.

Length:
Keep the answer concise and under 80 words.

Important:
Do not use information that is not present in the retrieved context.
If the context does not contain the answer, say that the information is not available.

Example:
User: What is the standard delivery fee?
Context: Standard delivery is free over INR 149.
Answer: Standard delivery is free for orders over INR 149.

User question:
{query}
"""


DOCS_DIR = Path("docs")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="zepto_policies_cosine",
    metadata={"hnsw:space": "cosine"}
)


def load_documents():
    documents = []
    ids = []

    for file in sorted(DOCS_DIR.glob("*.txt")):
        text = file.read_text(encoding="utf-8").strip()

        documents.append(text)
        ids.append(file.stem)

    return documents, ids


def store_documents():
    documents, ids = load_documents()

    embeddings = embedding_model.encode(documents).tolist()

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    print(f"Loaded {len(documents)} documents into ChromaDB.")


class AssistantState(TypedDict):
    query: str
    intent: str
    answer: str
    sources: list
    confidence: float


class AssistantResponse(BaseModel):
    answer: str
    sources: list
    confidence: float


class AskRequest(BaseModel):
    query: str


def validate_llm_response(raw_response):
    for attempt in range(3):
        if isinstance(raw_response, dict):
            if (
                isinstance(raw_response.get("answer"), str)
                and isinstance(raw_response.get("sources"), list)
                and isinstance(raw_response.get("confidence"), (int, float))
                and 0 <= raw_response.get("confidence") <= 1
            ):
                return raw_response

        raw_response = {
            "error": f"Invalid response. Corrective instruction: return answer, sources, and confidence. Retry {attempt + 1}."
        }

    return {
        "answer": "ERROR: LLM response could not be validated after 3 attempts.",
        "sources": [],
        "confidence": 0.0
    }


def classify_intent(state: AssistantState):
    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support"
    ]

    if any(keyword in query for keyword in policy_keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        "query": state["query"],
        "intent": intent
    }


def retrieve_and_answer(state: AssistantState):
    query = state["query"]

    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    documents = results["documents"][0]
    sources = results["ids"][0]

    context = "\n\n".join(documents)

    prompt = build_prompt(query, context)

    top_document = documents[0]

    if MOCK_LLM:
        answer = f"Based on the retrieved context: {top_document[:200]}"
    else:
        answer = "Real LLM mode is not configured."

    return {
        "answer": answer,
        "sources": sources,
        "confidence": 1.0
    }


def direct_answer(state: AssistantState):
    return {
        "answer": "I can only answer questions about Zepto policies right now.",
        "sources": [],
        "confidence": 1.0
    }


def route_question(state: AssistantState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


graph_builder = StateGraph(AssistantState)

graph_builder.add_node("classify_intent", classify_intent)
graph_builder.add_node("retrieve_and_answer", retrieve_and_answer)
graph_builder.add_node("direct_answer", direct_answer)

graph_builder.add_edge(START, "classify_intent")

graph_builder.add_conditional_edges(
    "classify_intent",
    route_question,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph_builder.add_edge("retrieve_and_answer", END)
graph_builder.add_edge("direct_answer", END)

graph = graph_builder.compile()


app = FastAPI(title="Zepto Support Assistant")


@app.post("/ask", response_model=AssistantResponse)
def ask_question(request: AskRequest):
    result = graph.invoke({
        "query": request.query,
        "intent": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    })

    response = AssistantResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

    return response


if __name__ == "__main__":
    store_documents()

    result = graph.invoke({
        "query": "What is the capital of India?",
        "intent": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0
    })

    response = AssistantResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

    print("\nValidated Response:")
    print(response.model_dump())
