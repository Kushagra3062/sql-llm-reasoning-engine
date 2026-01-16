from utilis.get_llm import get_llm
from pydantic import BaseModel

class Output_query(BaseModel):
    query_generated: str
    
def sql_generator(state:State):
    
    llm = get_llm()
    
    plan = state["plan"]
    schema = state["schema"]
    cleaned_question = state["cleaned_question"]
    
    prompt = f"""
        You are an expert SQL generator.

        Use ONLY the tables and columns from the schema below.
        Follow the plan EXACTLY.
        Always use explicit column names.
        
        Schema:
        {schema}

        Plan:
        {plan}

        Question:
        {cleaned_question}

        Generate a single safe SQL query.
    """
    response = llm.with_structured_output(Output_query).invoke({"input":prompt})
    
    return {
        "sql_query": response.query_generated
    }