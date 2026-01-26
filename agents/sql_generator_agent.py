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
        Generate the sql query using following rules:
            1. generate sql as per the steps
            2. don't use tables or columns apart from the schema
            3. always adhere to the intent
            4. use the query as well to look into it
            5. solve the error if any by analysing the error messages
              
        Use ONLY the tables and columns from the schema below.
        Follow the plan EXACTLY.
        Always use explicit column names.
        
        Schema:
        {schema}

        Plan:
        {plan}

        Question:
        {user_ques}
        
        intent_summary:
        {intent_summary}
        
        error_messages:
        {errors}

        Generate a single safe SQL query.
        Use Output_query tool to provide the output
    """
    response = llm.with_structured_output(Output_query).invoke(prompt)
    
    return {
        "sql_query": response.query_generated
    }