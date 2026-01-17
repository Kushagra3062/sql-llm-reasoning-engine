import re
from collections import deque

def find_relevant_tables(question, tables, fk_graph, max_depth=2):
    """
    Picks tables by fuzzy matching and FK neighborhood expansion.
    Avoids hallucinating unrelated tables.
    """

    words = set(re.findall(r"[a-zA-Z]+", question.lower()))

    # Direct hits = table name inside query words
    direct_hits = [
        t for t in tables 
        if any(t in w or w in t for w in words)
    ]

    # If no direct hits, fallback to return all tables (safe)
    if not direct_hits:
        return []

    # BFS expansion on FK graph
    expanded = set(direct_hits)
    queue = deque(direct_hits)

    while queue:
        t = queue.popleft()
        for neighbor in fk_graph.get(t, []):
            if neighbor not in expanded:
                expanded.add(neighbor)
                queue.append(neighbor)
                if len(expanded) >= 6:   # small guardrail
                    break

    return list(expanded)


#######################################################################
# 4️⃣ Validate plan from planner LLM
#######################################################################
def validate_plan(plan, schema):
    tables = schema["tables"]
    columns = schema["columns"]
    fks = schema["foreign_keys"]

    # ---- Validate tables exist ----
    for t in plan.get("tables", []):
        if t not in tables:
            raise ValueError(f"❌ Invalid table: {t}")

    # ---- Prevent duplicate tables ----
    if len(plan.get("tables", [])) != len(set(plan.get("tables", []))):
        raise ValueError("❌ Duplicate tables found in plan")

    # ---- Validate joins match FK constraints ----
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
            raise ValueError(f"❌ Bad join format: {join}")

        if (left_table, right_table) not in valid_pairs:
            raise ValueError(f"❌ Invalid FK join: {join}")

    # ---- Validate filters use valid tables ----
    for f in plan.get("filters", []):
        tokens = re.findall(r"([a-zA-Z0-9_]+)\.", f)
        for t in tokens:
            if t not in plan.get("tables", []):
                raise ValueError(f"❌ Filter references unknown table: {f}")

    # ---- Aggregation & GROUP BY rules ----
    if plan.get("aggregations"):
        # If aggregating AND selecting non-aggregate columns → need group_by
        if not plan.get("group_by"):
            # Allow pure COUNT(*)
            if not any("count" in agg.lower() for agg in plan["aggregations"]):
                raise ValueError("❌ Aggregation requires GROUP BY")

    return plan


#######################################################################
# 5️⃣ Enforce defaults & sanitize missing values
#######################################################################
def enforce_defaults(plan):
    # Always limit result size
    if not plan.get("limit"):
        plan["limit"] = 50

    # Remove joins if only 1 table selected
    if len(plan.get("tables", [])) <= 1:
        plan["joins"] = []

    # Fill missing standard keys
    for key in ["filters", "aggregations", "group_by"]:
        if plan.get(key) is None:
            plan[key] = []

    if "order_by" not in plan:
        plan["order_by"] = None

    return plan


#######################################################################
# 6️⃣ Debug helper to print schema
#######################################################################
def print_schema(schema):
    print("\n=== Tables ===")
    for t in schema["tables"]:
        print(t)

    print("\n=== Columns ===")
    for t,c in schema["columns"].items():
        print(t, c)

    print("\n=== Foreign Keys ===")
    print(schema["foreign_keys"])


# =====================================================
# planner_agent.py (UNCHANGED)
# =====================================================

from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os, json
from langchain_groq import ChatGroq

# Use STATIC SCHEMA instead of DB
from agents.schema_static import schema_static

load_dotenv()

###########################################
# GROQ CLIENT (via LangChain)
###########################################

llm = ChatGroq(
    model="openai/gpt-oss-120b",   # high quality, free
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

###########################################
# STATE STRUCTURE
###########################################
###########################################
# STATE STRUCTURE
###########################################
class PlannerState(dict):
    question: str
    schema: dict
    relevant_tables: list
    plan: dict
    error: str = ""
    retry_count: int = 0

###########################################
# STEP 1 — Load Static Schema
###########################################
def load_schema(state: PlannerState):
    state["schema"] = schema_static
    state["fk_graph"] = schema_static["fk_graph"]
    return state

###########################################
# STEP 2 — Identify Relevant Tables
###########################################
def pick_tables(state: PlannerState):
    schema = state["schema"]
    state["relevant_tables"] = find_relevant_tables(
        state["question"],
        schema["tables"],
        schema["fk_graph"],
        max_depth=2
    )
    return state

###########################################
# STEP 3 — LLM Planner (JSON PLAN)
###########################################
def call_planner(state: PlannerState):
    tables = state["relevant_tables"]
    columns = {t: state["schema"]["columns"][t] for t in tables}
    fks = state["schema"]["foreign_keys"]
    
    # Construct the instruction
    error_context = ""
    if state.get("error"):
        error_context = f"\n❌ PREVIOUS ATTEMPT REJECTED: {state['error']}\nFix the JSON plan based on this error."

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
        # Simple/Naive JSON extraction if LLM adds wrappers
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        state["plan"] = json.loads(text)
        state["error"] = "" # Clear error if parsing succeeds (validation comes next)
    except Exception as e:
        state["error"] = f"JSON Parsing Failed: {str(e)}"
        # We don't raise here, we let the validation/retry loop handle it if we want, or just retry immediately
        # But for now let's just let it fall through to validation failure or retry logic
    
    return state

###########################################
# STEP 4 — Validate + sanitize
###########################################
def validate_and_fix(state: PlannerState):
    if state.get("error"):
         # If JSON parsing failed, just return to trigger retry
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

###########################################
# BUILD LANGGRAPH
###########################################
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
