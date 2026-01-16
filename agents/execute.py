from tools.connect_db import connect_db
from schema import State

def execute_query(state: State):
    print("\n[MAIN] Node: Executing SQL")
    try:
        db = connect_db()
        # Use safe_sql_query if your safety check produced it, 
        # otherwise use sql_query
        query = state.get('safe_sql_query') or state.get('sql_query')
        
        if not query:
            return {"error": "No SQL query found to execute"}

        # Run the query
        data = db.run(query)
        
        return {
            "execution": True, 
            "data": data, 
            "error": "" # Clear any previous errors on success
        }
    except Exception as e:
        # Capture the specific DB error (e.g., Syntax error, Type mismatch)
        error_msg = str(e)
        print(f"❌ Execution Error: {error_msg}")
        
        return {
            "execution": False,
            "error": f"Database Execution Error: {error_msg}"
        }
        