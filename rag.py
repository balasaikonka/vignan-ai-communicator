# rag.py
# RAG Engine — loads vignan_university_knowledge.txt into ChromaDB
# and retrieves relevant chunks to answer parent questions

import os
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_knowledge_file(filepath: str = "vignan_university_knowledge.txt") -> str:
    """Read the university knowledge base text file."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def build_rag_engine(filepath: str = "vignan_university_knowledge.txt"):
    """
    Load the university knowledge document into ChromaDB.
    Uses free sentence-transformers embeddings — no API key needed.
    Returns a ChromaDB vector store ready for semantic search.
    """
    # Load text from file
    raw_text = load_knowledge_file(filepath)
    if not raw_text:
        print(f"Warning: Knowledge file '{filepath}' not found or empty.")
        raw_text = "No knowledge base loaded."

    # Split into small chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=60,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(raw_text)

    # Wrap into LangChain Document objects
    docs = [
        Document(page_content=chunk, metadata={"source": "vignan_knowledge"})
        for chunk in chunks
    ]

    # Load free local embeddings (downloads ~90MB once)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # Store in ChromaDB (in-memory)
    client = chromadb.Client()
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        client=client,
        collection_name="vignan_kb"
    )

    print(f"✅ RAG ready — {len(docs)} chunks loaded from '{filepath}'")
    return vector_store


def get_context(vector_store, question: str, top_k: int = 4) -> str:
    """
    Search ChromaDB for the most relevant chunks for a given question.
    Returns them joined as a single context string.
    """
    results = vector_store.similarity_search(question, k=top_k)
    if not results:
        return ""
    return "\n\n".join([doc.page_content for doc in results])
