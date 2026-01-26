from utilis.get_llm import get_llm
from pydantic import BaseModel
from schema import State

class Output_query(BaseModel):
    query_generated: str
    
def sql_generator(state:State):
    
    llm = get_llm()
    
    plan = state["plan"]
    schema = state["schema"]
    intent_summary = state["intent_summary"]
    user_ques = state["user_query"]
    errors = state['error']
    
    prompt = f"""
        You are an expert SQL generator.
        Your task is to generate a valid SQL query based on the schema and plan provided.
        
        CRITICAL RULES:
        1. You MUST generate a SQL query. Do NOT ask clarification questions.
        2. Ambiguity has ALREADY been resolved in a previous step. Assume the plan is final.
        3. If you are unsure, make a reasonable assumption based on the intent_summary and generate the SQL.
        4. Use ONLY the tables and columns from the schema below.
        5. Follow the plan EXACTLY.
        6. Always use explicit column names (table.column).
        7. Respond ONLY with the Output_query tool. Do not provide conversational text.
        
        Schema:
        {schema}

        Plan:
        {plan}

        Question:
        {user_ques}
        
        Intent Summary (Use this for context):
        {intent_summary}
        
        Previous Errors (if any):
        {errors}

        Generate the SQL query now.
    """
    response = llm.with_structured_output(Output_query).invoke(prompt)
    
    return {
        "sql_query": response.query_generated
    }