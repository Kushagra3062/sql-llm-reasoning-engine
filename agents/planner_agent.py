import re
from collections import deque

def find_relevant_tables(question, tables, fk_graph, max_depth=2):
    

    words = set(re.findall(r"[a-zA-Z]+", question.lower()))

    
    direct_hits = [
        t for t in tables 
        if any(t in w or w in t for w in words)
    ]

    
    if not direct_hits:
        return []

    
    expanded = set(direct_hits)
    queue = deque(direct_hits)

    while queue:
        t = queue.popleft()
        for neighbor in fk_graph.get(t, []):
            if neighbor not in expanded:
                expanded.add(neighbor)
                queue.append(neighbor)
                if len(expanded) >= 6:   
                    break

    return list(expanded)



def validate_plan(plan, schema):
    tables = schema["tables"]
    columns = schema["columns"]
    fks = schema["foreign_keys"]

   
    for t in plan.get("tables", []):
        if t not in tables:
            raise ValueError(f"Invalid table: {t}")

    
    if len(plan.get("tables", [])) != len(set(plan.get("tables", []))):
        raise ValueError("Duplicate tables found in plan")

    
    valid_pairs = {
        (fk["from_table"], fk["to_table"]) for fk in fks
    } | {
        (fk["to_table"], fk["from_table"]) for fk in fks
    }

    for join in plan.get("joins", []):
        try:
            left, right = join.split("=")
            left_table = left.strip().split(".")[0]
            right_table = right.strip().split(".")[0]
        except:
            raise ValueError(f"Bad join format: {join}")

        if (left_table, right_table) not in valid_pairs:
            raise ValueError(f"Invalid FK join: {join}")

    
    for f in plan.get("filters", []):
        tokens = re.findall(r"([a-zA-Z0-9_]+)\.", f)
        for t in tokens:
            if t not in plan.get("tables", []):
                raise ValueError(f"Filter references unknown table: {f}")

   
    if plan.get("aggregations"):
        
        if not plan.get("group_by"):
            
            if not any("count" in agg.lower() for agg in plan["aggregations"]):
                raise ValueError("Aggregation requires GROUP BY")

    return plan



def enforce_defaults(plan):
    
    if not plan.get("limit"):
        plan["limit"] = 50

    
    if len(plan.get("tables", [])) <= 1:
        plan["joins"] = []

    
    for key in ["filters", "aggregations", "group_by"]:
        if plan.get(key) is None:
            plan[key] = []

    if "order_by" not in plan:
        plan["order_by"] = None

    return plan



def print_schema(schema):
    print("\n=== Tables ===")
    for t in schema["tables"]:
        print(t)

    print("\n=== Columns ===")
    for t,c in schema["columns"].items():
        print(t, c)

    print("\n=== Foreign Keys ===")
    print(schema["foreign_keys"])




from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os, json
from langchain_groq import ChatGroq


from agents.schema_static import schema_static

load_dotenv()



llm = ChatGroq(
    model="openai/gpt-oss-120b",   
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


class PlannerState(dict):
    question: str
    schema: dict
    relevant_tables: list
    plan: dict
    error: str = ""
    retry_count: int = 0


def load_schema(state: PlannerState):
    state["schema"] = schema_static
    state["fk_graph"] = schema_static["fk_graph"]
    return state


def pick_tables(state: PlannerState):
    schema = state["schema"]
    state["relevant_tables"] = find_relevant_tables(
        state["question"],
        schema["tables"],
        schema["fk_graph"],
        max_depth=2
    )
    return state


def call_planner(state: PlannerState):
    tables = state["relevant_tables"]
    columns = {t: state["schema"]["columns"][t] for t in tables}
    fks = state["schema"]["foreign_keys"]
    
   
    error_context = ""
    if state.get("error"):
        error_context = f"\nPREVIOUS ATTEMPT REJECTED: {state['error']}\nFix the JSON plan based on this error."

    formatted_prompt = f"""
    ### TASK
    You are a Lead Database Architect. Your goal is to map complex natural language questions into a structured logical plan.
    ### CONTEXT
    User Question: {state['question']}
    Schema: {state['schema']}
    Schema tables allowed: {tables}
    Columns: {columns}
    Foreign keys: {fks}
    {error_context}

    ### OPERATIONAL GUIDELINES for COMPLEX TASKS:
    1. FK-CHAIN VERIFICATION: For multi-table joins, list the intermediate "bridge" tables even if no columns are selected from them.
    2. AGGREGATION HIERARCHY: If the question involves "average of totals" or "max of counts," specify the grain of the GROUP BY clearly.
    3. COMPARATIVE LOGIC: If the user asks for "More than X," "Higher than average," or "Not in," use the 'filters' array to describe the logical comparison.
    4. AMBIGUITY TRIAGE: If a term like "Top" could mean "By Revenue" or "By Unit Volume" and BOTH exist in the schema, you MUST set "needs_clarification": true.

    ### DRAFTING PROCESS (Internal Monologue):
    - Step 1: Identify the target metric (What are we counting/summing?).
    - Step 2: Trace the FK path from the target metric table back to the entity table.
    - Step 3: Check for logical filters (Dates, status codes, specific names).
    - Step 4: Validate that every column used is inside the 'tables' list.
    
    ### CRITICAL RULE:
    - If you include 'aggregations', you MUST include 'group_by' unless the aggregation is a global count (e.g. COUNT(*)).
    - The 'group_by' list must include ALL non-aggregated columns selected or implied.

    ### OUTPUT FORMAT (JSON ONLY):
    {{
    "tables": ["list", "of", "tables"],
    "joins": ["tableA.id = tableB.fk_id"],
    "filters": ["expression using table.column"],
    "aggregations": ["SQL-like aggregation string"],
    "group_by": ["columns to group by"],
    "order_by": {{"column": "name", "direction": "desc"}},
    "limit": 50,
    "needs_clarification": false,
    "needs_exploration": false,
    "steps": "Briefly Explain the steps to generate the query like human but optimal query",
    "explain": "Briefly explain the join path and logic used."
    }}
"""

    response = llm.invoke(formatted_prompt)
    text = response.content

    try:
       
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        state["plan"] = json.loads(text)
        state["error"] = "" 
    except Exception as e:
        state["error"] = f"JSON Parsing Failed: {str(e)}"
        
    
    return state


def validate_and_fix(state: PlannerState):
    if state.get("error"):
         
         state["retry_count"] = state.get("retry_count", 0) + 1
         return state

    try:
        validate_plan(state["plan"], state["schema"])
        state["plan"] = enforce_defaults(state["plan"])
    except ValueError as e:
        state["error"] = str(e)
        state["retry_count"] = state.get("retry_count", 0) + 1
    
    return state

def should_retry(state: PlannerState):
    if state.get("error") and state.get("retry_count", 0) < 3:
        return "call_planner"
    return END


workflow = StateGraph(PlannerState)

workflow.add_node("load_schema", load_schema)
workflow.add_node("pick_tables", pick_tables)
workflow.add_node("call_planner", call_planner)
workflow.add_node("validate", validate_and_fix)

workflow.set_entry_point("load_schema")
workflow.add_edge("load_schema", "pick_tables")
workflow.add_edge("pick_tables", "call_planner")
workflow.add_edge("call_planner", "validate")
workflow.add_conditional_edges("validate", should_retry, {
    "call_planner": "call_planner",
    END: END
})

planner_graph = workflow.compile()
