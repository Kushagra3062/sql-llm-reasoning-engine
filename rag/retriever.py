from rag.vectordb import get_vector_store

def retrieve_documents(query: str, k: int = 3):
    print(f"[RAG] Retrieving top {k} documents for query: {query}")
    vector_store = get_vector_store()
    
    # Chroma retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    # Format into context string
    context = "\n\n".join([doc.page_content for doc in docs])
    return context
