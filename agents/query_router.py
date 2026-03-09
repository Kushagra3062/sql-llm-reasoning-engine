from pydantic import BaseModel, Field
from schema import State
from utilis.get_llm import get_llm
from agents.schema_static import schema_static

class RouteDecision(BaseModel):
    route: str = Field(description="One of: 'SQL_QUERY', 'MARKET_DATA', 'NEWS', 'GENERAL_INFO'")

def query_router_node(state: State):
    print("\n[ROUTER] Classifying User Intent...")
    query = state.get("resolved_query") or state.get("user_query", "")
    
    prompt = f"""
    You are an intelligent router for a hybrid analytical assistant.
    Analyze the following user query and classify it strictly into ONE of these four categories:
    
    1. SQL_QUERY: If the user is asking about structured database records like company financials, revenues, profits, market caps, ratios, etc.
       THE DATABASE SCHEMA IS:
       {schema_static['columns']}
       
       USE SQL_QUERY if the question can be answered by querying these specific columns for specific years or companies.
       
    2. MARKET_DATA: If the user is asking strictly about real-time or recent stock prices, trading volume, or market trends (Price history).
    3. NEWS: If the user is asking for the latest news, updates, or recent events covering a company or technology.
    4. GENERAL_INFO: If the user is asking for general information, history, or Wikipedia-style facts about a company.
    
    User Query: '{query}'
    
    Respond EXACTLY with the classification.
    """
    
    try:
         # Use structured output
         llm = get_llm()
         decision = llm.with_structured_output(RouteDecision).invoke(prompt)
         print(f"[ROUTER DEBUG] Raw Decision Output: {decision}")
         route = decision.route if hasattr(decision, 'route') else decision.get('route')
    except Exception as e:
         import traceback
         traceback.print_exc()
         print(f"[ROUTER] Error parsing route: {e}")
         route = "SQL_QUERY" # fallback to default

    print(f"[ROUTER] Decided Route: {route}")
    return {"route": route}
