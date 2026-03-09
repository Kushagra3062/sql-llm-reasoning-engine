from rag.retriever import retrieve_documents
from schema import State

def rag_agent(state: State):
    print("\n[RAG] Fetching external knowledge context...")
    # For RAG, raw user_query (e.g. 'Microsoft') provides better semantic matches than resolved tickers (e.g. 'MSFT')
    query = state.get("user_query") or state.get("resolved_query", "")
    
    try:
        context_str = retrieve_documents(query, k=3)
        if not context_str.strip():
             context_str = "No relevant context found in RAG database."
        return {"rag_context": context_str}
    except Exception as e:
        print(f"[RAG] Error during retrieval: {e}")
        return {"rag_context": f"Error retrieving context: {str(e)}"}
