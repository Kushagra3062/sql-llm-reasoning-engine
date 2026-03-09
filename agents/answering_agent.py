from utilis.get_llm import get_llm
from schema import State

def answer_generator(state: State):
    llm = get_llm()

    data = state.get("data", [])
    
    raw_data_str = str(data)
    limit = 8000 * 4 
    
    if len(raw_data_str) > limit:
        truncated_data = raw_data_str[:limit] + "\n... [Data Truncated for Length] ..."
    else:
        truncated_data = raw_data_str

    query_to_use = state.get("resolved_query") or state.get("user_query", "")
    route = state.get("route", "SQL_QUERY")
    
    # Conditional formatting based on the chosen route
    market_data_str = ""
    rag_context_str = ""
    sql_data_str = ""
    
    if route == "MARKET_DATA":
         market_data_str = f"Market Data Retrieved: {state.get('market_data', 'None')}"
    elif route in ["NEWS", "GENERAL_INFO"]:
         rag_context_str = f"RAG Document Context: {state.get('rag_context', 'None')}"
    else:
         sql_data_str = f"The SQL Plan was: {state.get('plan', '')}\nThe Database returned these results: {truncated_data}"
         
    prompt = f"""
    You are a Senior Data Analyst and Financial Advisor. 
    The user asked: {query_to_use}
    Intent_summary: {state.get('intent_summary', '')}
    Route used: {route}
    
    {sql_data_str}
    {market_data_str}
    {rag_context_str}

    YOUR TRAITS:
    Structure your answer as follows:
    1. **Direct Answer**: A concise summary of the result.

    2. **Key Insights**: Bullet points of interesting findings.

    3. **Data Table/List**: A clean presentation of the data (limit to top 10 rows if huge).
    
    IMPORTANT: 
    - The SQL was specifically written to only return items that satisfy the user's request.
    - Always insert TWO newlines before and after any Markdown table or list for correct alignment.
    - Do NOT include any meta-instructions or parentheticals in the final output.
    """

    ai_response = llm.invoke(prompt).content

    return {
        "final_response": ai_response
    }