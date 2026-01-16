import re
from schema import State

def is_safe_sql(sql):
    sql_lower = sql.lower()
    # 1. Block DML/DDL keywords (at start of statement or after semicolon)
    banned = [r"\binsert\b", r"\bupdate\b", r"\bdelete\b", r"\bdrop\b", r"\balter\b", r"\btruncate\b", r"\bcreate\b"]
    for pattern in banned:
        if re.search(pattern, sql_lower):
            return False
            
    # 2. Block multiple statements (Semicolon injection)
    if sql.strip().count(';') > 1 or (sql.strip().count(';') == 1 and not sql.strip().endswith(';')):
        return False
        
    return True

def has_proper_limit(sql):
    sql_clean = sql.lower().strip().rstrip(';')
    # Check if 'limit' exists at the end of the query
    if "limit" not in sql_clean:
        return False
    return True

def enforce_safety_limits(sql, default_limit=10):
    if not has_proper_limit(sql):
        # Remove trailing semicolon and add limit
        return sql.strip().rstrip(';') + f" LIMIT {default_limit};"
    return sql

def table_exist(state:State): # has to pass the state as well
    
    tables = state["tables"]
    schema = state["schema"]
    
    if not tables:
        return [True, None]
    for table in tables:
        if table not in schema:
            return [False,table]
    
    return [True,None] 

def col_exist(state:State): # has to pass the state as well
    
    # Create a set of all column names in the schema
    all_schema_columns = set()
    schema = state["schema"]
    
    for table, cols in schema.items():
        for col_name, _ in cols:
            all_schema_columns.add(col_name)

    # Now check each column
    columns = state['columns']
    for col in columns:
        if col not in all_schema_columns:
            return [False,col]

    return [True,None]

def safety_check(state:State):
    
    sql_query = state['sql_query']
    
    if not is_safe_sql(sql_query):
        #GO BACK TO GENRATOR AGAIN
        state['error'] = "Unsafe SQL: DDL/DML detected"
        return state
    bg,tb = table_exist(state)
    if not bg:
        #GO BACK TO GENRATOR AGAIN
        state['error'] = f"{tb} Table does not exists"
        return state
    
    if not has_proper_limit(sql_query):
        state['sql_query'] = enforce_safety_limits(sql_query)
    
    return {
        'ready' : True,
        'safe_sql_query': state['sql_query'],
        "error": ""
    } 
    
    
    

    