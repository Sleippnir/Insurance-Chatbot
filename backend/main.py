import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.generators.llama_cpp import LlamaCppGenerator
from haystack_chroma import ChromaDocumentStore
from haystack_chroma.retriever import ChromaQueryTextRetriever

# --- Haystack RAG Pipeline Setup ---

# This global variable will hold the initialized RAG pipeline.
rag_pipeline = None

def build_rag_pipeline():
    """
    Builds and returns a Haystack RAG (Retrieval-Augmented Generation) pipeline.
    The pipeline retrieves relevant documents from ChromaDB and uses them to
    generate a response with a Large Language Model.
    """
    document_store = ChromaDocumentStore(persist_path="chroma_db")

    # 1. Retriever: Fetches relevant documents from the vector store.
    retriever = ChromaQueryTextRetriever(document_store=document_store, top_k=5)

    # 2. Prompt Builder: Creates a prompt for the LLM using the retrieved documents.
    template = """
    Using only the context provided, please generate a concise insurance policy document
    that addresses the user's query. Do not use any external knowledge.

    Context:
    {% for doc in documents %}
        - {{ doc.content }}
    {% endfor %}

    Query: {{ query }}

    Generated Policy:
    """
    prompt_builder = PromptBuilder(template=template)

    # 3. LLM Generator: Generates text based on the prompt.
    # IMPORTANT: This component requires a Llama 3 GGUF model file.
    # The path to the model should be set in an environment variable `LLM_MODEL_PATH`.
    # If the variable is not set, the generator will not be added to the pipeline,
    # and the API will return retrieved documents instead of a generated policy.
    llm = None
    model_path = os.getenv("LLM_MODEL_PATH")
    if model_path and os.path.exists(model_path):
        llm = LlamaCppGenerator(model_path=model_path, n_ctx=2048)
    else:
        print("Warning: LLM_MODEL_PATH is not set or the file does not exist.")
        print("The RAG pipeline will run without the generator.")

    # 4. Build the Pipeline
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.connect("retriever.documents", "prompt_builder.documents")

    if llm:
        pipeline.add_component("llm", llm)
        pipeline.connect("prompt_builder.prompt", "llm.prompt")

    return pipeline

# --- FastAPI Application ---

app = FastAPI(
    title="Insurance Policy Generation Chatbot API",
    description="An API for generating insurance policies using a RAG pipeline.",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event():
    """
    Initializes the RAG pipeline when the FastAPI application starts.
    """
    global rag_pipeline
    rag_pipeline = build_rag_pipeline()
    print("RAG pipeline built successfully.")

class PolicyRequest(BaseModel):
    query: str

class PolicyResponse(BaseModel):
    policy: str
    retrieved_documents: List[Dict[str, Any]]

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the Insurance Policy Generation Chatbot API"}

@app.post("/generate_policy", response_model=PolicyResponse)
async def generate_policy(request: PolicyRequest):
    """
    Generates an insurance policy based on a user's query by running the RAG pipeline.
    If an LLM is configured, it returns a generated policy. Otherwise, it returns
    the documents retrieved from the knowledge base.
    """
    if rag_pipeline is None:
        raise HTTPException(status_code=500, detail="RAG pipeline is not initialized.")

    # The components to run depend on whether the LLM is available
    if "llm" in rag_pipeline.components:
        # Run the full pipeline
        result = rag_pipeline.run({
            "retriever": {"query": request.query},
            "prompt_builder": {"query": request.query}
        })
        policy = result["llm"]["replies"][0]
        retrieved_docs = result["retriever"]["documents"]
    else:
        # Run only the retrieval part
        result = rag_pipeline.run({"retriever": {"query": request.query}})
        policy = "LLM generator is not configured. The following documents were retrieved from the knowledge base based on your query."
        retrieved_docs = result["retriever"]["documents"]

    # Convert Haystack Document objects to dictionaries for the response
    retrieved_docs_dict = [doc.to_dict() for doc in retrieved_docs]

    return {"policy": policy, "retrieved_documents": retrieved_docs_dict}
