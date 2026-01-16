from langgraph.graph import StateGraph, START, END
from agents.explore_agent import exp_agent
from agents.dsds import create_smart_refiner
from langgraph.checkpoint.memory import MemorySaver
from schema import State

# Placeholder for your SQL Generator Agent
def sql_generator_node(state: State):
    print("\n[MAIN] Node: SQL Generation")
    # Here you would take state['intent_summary'] and state['tables'] 
    # and use a prompt to generate the actual PostgreSQL code.
    return {"sql_query": "SELECT ..."}

graph_b = StateGraph(State)

# Nodes
graph_b.add_node("explore", exp_agent)
graph_b.add_node("ambiguity", create_smart_refiner(State))
graph_b.add_node("generate_sql", sql_generator_node)

# Flow
graph_b.add_edge(START, "explore")
graph_b.add_edge("explore", "ambiguity")
graph_b.add_edge("ambiguity", "generate_sql")
graph_b.add_edge("generate_sql", END)

graph = graph_b.compile(checkpointer=MemorySaver())

# Execution
initial_state = {
    "user_query": "find artist of top 3 song?",
    "messages": [],
    "schema": {},
    "intent_summary": "", # Initialize to avoid KeyErrors
    "human_choice": 0
}
config = {"configurable": {"thread_id": "1"}}
final_state = graph.invoke(initial_state,config)

print(f"\n--- FINAL RESULTS ---")
print(f"Intent: {final_state.get('intent_summary')}")
print(f"Tables: {final_state.get('tables')}")
print(f"Assumptions: {final_state.get('assumptions')}")