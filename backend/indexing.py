import os
from pathlib import Path
from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack_chroma import ChromaDocumentStore

def run_indexing_pipeline():
    """
    Creates and runs a Haystack pipeline to index text files from the 'data' directory
    into a ChromaDB vector store.
    """
    # Initialize the document store. It will be created in a 'chroma_db' directory.
    document_store = ChromaDocumentStore(persist_path="chroma_db")

    # Define the indexing pipeline
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("converter", TextFileToDocument())
    indexing_pipeline.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=10, split_overlap=2))
    indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder(model="all-MiniLM-L6-v2"))
    indexing_pipeline.add_component("writer", DocumentWriter(document_store))

    # Connect the components in the correct order
    indexing_pipeline.connect("converter.documents", "splitter.documents")
    indexing_pipeline.connect("splitter.documents", "embedder.documents")
    indexing_pipeline.connect("embedder.documents", "writer.documents")

    # Identify the source files in the 'data' directory
    # Assumes this script is run from the project's root directory
    source_file_paths = list(Path("data").glob("*.txt"))

    if not source_file_paths:
        print("Warning: No .txt files found in the 'data' directory. The knowledge base will be empty.")
        return

    print(f"Starting indexing for the following files: {[str(p) for p in source_file_paths]}")

    # Run the pipeline
    indexing_pipeline.run({"converter": {"sources": source_file_paths}})

    print(f"Indexing complete. {len(document_store.get_all_documents())} documents have been indexed.")

if __name__ == "__main__":
    run_indexing_pipeline()
