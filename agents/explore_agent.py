from tools.db_tools import get_full_schema, get_foreign_keys, fetch_invoice_sample
from schema import State

def exp_agent(state:State):
    schema = get_full_schema()
    get_foreign_key = get_foreign_keys()
    
    
    return {
        "schema": schema,
        "foreign_keys": get_foreign_key
    }    