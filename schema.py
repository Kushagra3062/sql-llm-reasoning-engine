from typing import List, Dict, Optional, Annotated, TypedDict, Tuple, Any, Union
from enum import Enum
from pydantic import BaseModel, Field


class AgentDecision(str, Enum):
    MCQ_NEEDED = "generate_mcqs"
    ASSUME_SAFE = "safe_assumptions"
    READY = "planner_ready"


class RefinerOutput(BaseModel):
    decision: AgentDecision
    confidence: float
    tables: List[str]
    intent_summary: str
    mcq_options: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list, description="List of assumptions made")
    temporal_snippet: str = ""


class State(TypedDict, total=False):
    # User side
    user_query: str

    # Schema side
    schema: Dict[str, List[Tuple[str, str]]]   # table -> [(col, type)]
    foreign_keys: List[Tuple[str, str, str, str]]  # optional but structured

    # Ambiguity output
    tables: List[str]
    intent_summary: str
    assumptions: List[str]
    temporal_snippet: str
    ready: bool

    # Planner
    plan: str

    # SQL side
    sql_query: str
    safe_sql_query: str
    execution: bool
    # Error handling
    error: str
    error_source: str

    # Reasoning / explainability
    reasoning_steps: List[str]
    messages: Annotated[List[str], "append"]

    # LLM side
    llm_output: RefinerOutput
    human_choice: Union[int, str]
    
    data: List[Any]
    final_response: str
    
    retry_count: int
