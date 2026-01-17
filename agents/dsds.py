import json
import ast
from typing import Dict, Literal

from schema import State, AgentDecision, RefinerOutput
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from utilis.get_llm import get_llm

llm = get_llm()

parser = PydanticOutputParser(pydantic_object=RefinerOutput)

DETECTION_PROMPT = ChatPromptTemplate.from_template("""

You are a High-Precision Ambiguity Detector for a SQL Database. 
Your goal is to protect the system from making incorrect guesses.

SCHEMA SUMMARY:
{schema}

USER QUERY:
"{query}"

CORE PRINCIPLE: 
If a human analyst would need to ask "What do you mean by X?" or "Which X?", 
then you MUST choose 'generate_mcqs'.

VAGUENESS RULES:
1. ENTITY IDENTIFIERS: If the user says "this", "that", or such kind of words 
   without providing a specific Name, ID or clarifing it refering to it is VAGUE.
2. RANKING TERMS: "Best", "Top", "Worst", "Most Popular" are VAGUE. 
   You must ask if they mean by 'Revenue', 'Count', or 'Rating'.
3. TEMPORAL TERMS: "Recent", "Old", "Latest" are VAGUE. 
   You must ask for a specific timeframe (e.g., 30 days vs 1 year).
4. AGGREGATIONS: "Total sales" is VAGUE if it's unclear whether it's 
   Total Quantity, Total Revenue, or Total after Tax.

DECISION LOGIC:
- If Rule 1, 2, 3, or 4 applies → decision: 'generate_mcqs'
- If the query is technically clear but has 2+ possible JOIN paths → decision: 'generate_mcqs'
- If the query provides specific names (e.g., 'AC/DC') and clear metrics (e.g., 'Total Spend') 
  and is 100% certain → decision: 'planner_ready'

{format_instructions}
""")

MCQ_PROMPT = ChatPromptTemplate.from_template("""
USER SELECTED OPTION {human_choice}

ORIGINAL QUERY:
"{query}"

SCHEMA:
{schema}

Map to tables and intent.

{format_instructions}
""")

detect_chain = DETECTION_PROMPT | llm | parser
mcq_chain = MCQ_PROMPT | llm | parser


def compress_schema(schema: Dict, max_cols_per_table: int = 6):
    compressed = {}
    for table, col_data in schema.items():
        
        if isinstance(col_data, str):
            try:
                cols = ast.literal_eval(col_data)
            except:
                cols = []
        else:
            cols = col_data
            
        formatted_cols = []
        for col in cols[:max_cols_per_table]:
            if isinstance(col, tuple) and len(col) == 2:
                formatted_cols.append(f"{col[0]}({col[1]})")
            else:
                formatted_cols.append(str(col))
        compressed[table] = formatted_cols
    return compressed

def detect_critical_ambiguity(state: State):
    print("\n[REFINER] Node: Detect Ambiguity")
    schema_summary = compress_schema(state["schema"])
    
    result = detect_chain.invoke({
        "query": state["user_query"],
        "schema": json.dumps(schema_summary, indent=2),
        "format_instructions": parser.get_format_instructions()
    })

  
    return {
        "llm_output": result,
        "messages": [f"Detected: {result.decision.value}"]
    }

def handle_human_mcqs(state: State):
    print("\n[REFINER] Node: Human Resolve")
    if not state.get("human_choice"): return state

    schema_summary = compress_schema(state["schema"])
    result = mcq_chain.invoke({
        "query": state["user_query"],
        "human_choice": state["human_choice"],
        "schema": json.dumps(schema_summary, indent=2),
        "format_instructions": parser.get_format_instructions()
    })

    return {
        "tables": result.tables,
        "intent_summary": result.intent_summary,
        "assumptions": result.assumptions,
        "ready": True
    }

def create_smart_refiner(State_Schema):
   
    graph = StateGraph(State_Schema)
    graph.add_node("detect", detect_critical_ambiguity)
    graph.add_node("human_resolve", handle_human_mcqs)
    return graph

def route_ambiguity_decision(state: State):
    if not state.get("llm_output"):
        return "sync_and_end"
    
    decision = state["llm_output"].decision
    if decision == AgentDecision.MCQ_NEEDED:
        return "human_resolve"
    
    
    return "sync_and_end"


def auto_resolve_safe_ambiguity(state: State):
    print("[REFINER] Syncing intent to main graph...")
    
    if not state.get("llm_output"):
         return {"ready": True, "intent_summary": state.get("user_query")} 
         
    out = state["llm_output"]
    return {
        "tables": out.tables,
        "intent_summary": out.intent_summary,
        "assumptions": out.assumptions,
        "temporal_snippet": "last 90 days" if "recent" in state["user_query"].lower() else "",
        "ready": True
    }