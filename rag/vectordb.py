import os
from langchain_community.vectorstores import Chroma
from rag.embeddings import get_embeddings
from rag.loaders import load_and_split_documents

# Cache the vector store to avoid rebuilding it on every query
_VECTOR_STORE = None

def get_vector_store():
    global _VECTOR_STORE
    
    if _VECTOR_STORE is not None:
        return _VECTOR_STORE
        
    embeddings = get_embeddings()
    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    
    # If DB already exists, load it
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        print("[RAG] Loading existing Chroma vector store...")
        _VECTOR_STORE = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        # Otherwise, build it
        print("[RAG] Building new Chroma vector store...")
        splits = load_and_split_documents()
        if not splits:
             print("[RAG] Warning: No documents loaded. Creating empty Chroma DB.")
             # Create empty so it doesn't fail, but warn
             _VECTOR_STORE = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        else:
             _VECTOR_STORE = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_dir)
             
    return _VECTOR_STORE
