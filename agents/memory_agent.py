import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from schema import State

llm = ChatGroq(
    model="openai/gpt-oss-120b", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

def session_initializer_node(state: State):
    return {
        "chat_history": [],
        "structured_context": {},
        "session_id": state.get("session_id", "default_session")
    }

def welcome_node(state: State):
    return {
        "final_response": "Hello! I am your AI SQL assistant. How can I help you query the database today?",
    }

def context_resolver_node(state: State):
    user_query = state.get("user_query", "")
    chat_history = state.get("chat_history", [])
    structured_context = state.get("structured_context", {})

    history_str = ""
    if chat_history:
        for msg in chat_history[-10:]:  # last 5 interactions
            role = "Human" if isinstance(msg, HumanMessage) else "AI"
            history_str += f"{role}: {msg.content}\n"
            
    # Load explicit company mapping config
    ticker_mapping = {
        "Apple": "AAPL", "Microsoft": "MSFT", "Google": "GOOG", "Alphabet": "GOOG",
        "PayPal": "PYPL", "AIG": "AIG", "PG&E": "PCG", "Sears": "SHLDQ", 
        "McDonalds": "MCD", "McDonald's": "MCD", "Barclays": "BCS", 
        "Nvidia": "NVDA", "NVIDIA": "NVDA", "Intel": "INTC", "Amazon": "AMZN"
    }
    prompt = f"""
    You are an AI context resolution agent for a SQL database.
    Your task is to take a new user question and resolve any missing context (like company names, entities, timeframes) using the chat history and structured context.
    
    ### CONTEXT
    Chat History:
    {history_str}
    
    Structured Entities:
    {json.dumps(structured_context)}
    
    Company Ticker Mappings:
    {json.dumps(ticker_mapping)}
    
    New Question: {user_query}
    
    ### INSTRUCTIONS
    1. If the new question refers to an entity mentioned previously (e.g., "now show it for 2023" or "what about its revenue"), replace pronouns or implied context with the actual entities.
    2. Extract any new entities from the current question to update the structured context. Do not store raw SQL or outputs.
    3. TICKER MAPPING: If the user explicitly mentions a company name (e.g., 'Apple', 'Google'), you MUST replace the name with its corresponding Ticker Symbol (e.g., 'AAPL', 'GOOG') using the mapping provided above in the `resolved_query`.
    4. Return ONLY a JSON object with two keys:
       - "resolved_query": The fully standalone question with all context injected, AND heavily mapping natural language companies to tickers.
       - "new_entities": A dictionary of any key entities (company, metric, time period, region) mentioned in the latest question or carried over.
       
    ### OUTPUT FORMAT (JSON ONLY)
    {{
        "resolved_query": "standalone question here",
        "new_entities": {{"entity_type": "entity_value"}}
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        text = response.content
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        result = json.loads(text.strip())
        
        resolved_query = result.get("resolved_query", user_query)
        new_entities = result.get("new_entities", {})
        
        updated_context = {**structured_context, **new_entities}
        
    except Exception as e:
        print(f"[MEMORY] Context Resolution Failed: {e}")
        resolved_query = user_query
        updated_context = structured_context
        
    return {
        "resolved_query": resolved_query,
        "structured_context": updated_context
    }

def memory_updater_node(state: State):
    chat_history = state.get("chat_history", [])
    user_query = state.get("user_query", "")
    final_response = state.get("final_response") or state.get("intent_summary") or "No response"
    
    # Don't append empty user queries (like from welcome node triggers)
    if user_query:
        chat_history.append(HumanMessage(content=user_query))
        chat_history.append(AIMessage(content=final_response))
    
    # Trim to last 5 interactions (1 interaction = 1 Human + 1 AI = 2 messages, so 10 messages max)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
        
    return {"chat_history": chat_history}
