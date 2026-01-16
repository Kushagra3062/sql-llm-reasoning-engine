from langgraph.graph import StateGraph, START, END
from agents.explore_agent import exp_agent
from agents.dsds import create_smart_refiner
from langgraph.checkpoint.memory import MemorySaver
from schema import State
from agents.planner_agent import planner_graph
from agents.sql_generator_agent import sql_generator
from agents.safty_agent import safety_check
from agents.execute import execute_query
from agents.answering_agent import answer_generator

# Placeholder for your SQL Generator Agent
def sql_generator_node(state: State):
    print("\n[MAIN] Node: SQL Generation")
    # Here you would take state['intent_summary'] and state['tables'] 
    # and use a prompt to generate the actual PostgreSQL code.
    return {"sql_query": "SELECT ..."}

def call_planner_subgraph(state: State):
    """
    Bridge between the Main State and the Planner Subgraph.
    """
    print("\n[MAIN] Node: Planning SQL Structure")
    
    retries = state.get("retry_count",0)
    # 1. Prepare input for the planner subgraph
    # We use the 'intent_summary' from the refiner as the question
    question = state.get("intent_summary") or state["user_query"]
    if retries > 0:
        question += f" (IMPORTANT: Your previous plan returned 0 rows. Please check table joins and filter case-sensitivity.)"
    planner_input = {
        "question": question,
        "schema": state["schema"], # Pass the full schema
        "relevant_tables": state.get("tables", []) # Use tables picked by Refiner
    }

    # 2. Invoke the compiled planner graph
    # Import 'planner_graph' from your planner_agent.py
    planner_result = planner_graph.invoke(planner_input)

    # 3. Return the plan back to the main state
    generated_plane = planner_result["plan"]
    return {
        "plan": generated_plane,
        "tables": generated_plane.get("tables", []),
        "retry_count": retries+1,
        "messages": [f"📝 Plan generated with {len(planner_result['plan'].get('joins', []))} joins."]
    }
    
graph_b = StateGraph(State)

# Nodes
graph_b.add_node("explore", exp_agent)
graph_b.add_node("ambiguity", create_smart_refiner(State))
graph_b.add_node("planner", call_planner_subgraph) # The bridge node
graph_b.add_node("generate_sql", sql_generator)
graph_b.add_node("safety",safety_check)
graph_b.add_node("execute",execute_query)
graph_b.add_node("answer",answer_generator)


# Flow
graph_b.add_edge(START, "explore")
graph_b.add_edge("explore", "ambiguity")
graph_b.add_edge("ambiguity", "planner")

# After planning is done, go to final SQL generation
graph_b.add_edge("planner", "generate_sql")
graph_b.add_edge("generate_sql", "safety")

def route_after_safety(state: State):
    # If there is an error message, go back to 'generate_sql'
    if not state.get("ready"):
        print(f"[SAFETY] Error found: {state['error']}. Re-routing to Generator...")
        return "generate_sql"
    
    # Otherwise, proceed to the end (or to an executor node)
    return "execute"

def route_after_execution(state: State):
    # If a database error occurred during runtime
    retries = state['retry_count']
    if state.get("error") and not state.get("execution"):
        print(f"❌ [EXECUTION] DB Error: {state['error']}. Retrying Generator...")
        return "generate_sql"
    if not state['data'] or len(state['data']) == 0:
        if retries < 4:
            print(f"⚠️ [EMPTY DATA] Attempt {retries + 1}/3. Re-routing to Planner...")
            return "planner"
        else:
            print("🚫 [EMPTY DATA] Max retries reached. Proceeding to answer with empty state.")
            return "answer"
    
    # CASE 3: Success!
    return "answer"
    

graph_b.add_conditional_edges(
    "safety", 
    route_after_safety,
    {
        "generate_sql": "generate_sql", # Loop back if unsafe
        "execute": "execute"            # Proceed if safe
    }
)

# --- Conditional Routing: Execution to End ---
graph_b.add_conditional_edges(
    "execute",
    route_after_execution,
    {
        "generate_sql": "generate_sql", # Loop back if DB error occurs
        "planner": "planner",
        "answer": "answer"                        # Finish if data is fetched
    }
)

graph_b.add_edge("answer",END)

graph = graph_b.compile(checkpointer=MemorySaver())

# Execution
initial_state = {
    "user_query": "Are there any genres with no sales?",
    "messages": [],
    "schema": {},
    "intent_summary": "", # Initialize to avoid KeyErrors
    "human_choice": 0,
    "retry_count": 0,
    "error": ""
}
config = {"configurable": {"thread_id": "1"}}
final_state = graph.invoke(initial_state,config)

print(f"\n--- FINAL RESULTS ---")
print(f"Intent: {final_state.get('intent_summary')}")
print(f"Tables: {final_state.get('tables')}")
print(f"Assumptions: {final_state.get('assumptions')}")
print(f"Plan: {final_state.get('plan')}")
print(f"Query: {final_state.get('sql_query')}")
print(f"Data: {final_state.get('data')}")
print(f"Final Report: {final_state.get('final_response')}")