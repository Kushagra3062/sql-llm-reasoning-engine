from utilis.get_llm import get_llm
from schema import State

def answer_generator(state: State):
    llm = get_llm()
    # Get raw data (likely list of tuples)
    data = state.get("data", [])
    
    # --- 1. SIMPLE TRUNCATION (8k tokens ~ 32k characters) ---
    raw_data_str = str(data)
    limit = 8000 * 4 
    
    if len(raw_data_str) > limit:
        truncated_data = raw_data_str[:limit] + "\n... [Data Truncated for Length] ..."
    else:
        truncated_data = raw_data_str

    # --- 2. NO-NONSENSE PROMPT ---
    prompt = f"""
    You are a Senior Data Analyst. 
    The user asked: {state['user_query']}
    It's Intent_summary: {state['intent_summary']}
    The SQL Plan was: {state['plan']}
    The Database returned these results: {truncated_data}

    YOUR TRAITS:
    - You answer must be strictly in a clear, displayable and Point-Wise manner.
    - You use Markdown tables if the data is substantial.
    - You provide a summary first, then the details.
    - You DO NOT dump raw text chunks.
    - You DO NOT dump raw text chunks.
    

    Structure your answer as follows:
    1. **Direct Answer**: A concise summary of the result.
    2. **Key Insights**: Bullet points of interesting findings.(Strictly do this)
    3. **Data Table/List**: A clean presentation of the data (limit to top 10 rows if huge).(It must be strictly in a clear, displayable and Point-Wise manner.)
    
    IMPORTANT: 
    The SQL was specifically written to only return items that satisfy the user's request.
    Interpret the results based on the SQL logic used.
    """

    # --- 3. EXECUTE ---
    ai_response = llm.invoke(prompt).content

    return {
        "final_response": ai_response
    }