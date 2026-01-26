from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from .connect_db import get_db

# db = connect_db() # Removed global instance

def get_tables():
    return get_db().get_usable_table_names()

def get_columns(table_name:str):
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}';
    """
    return get_db().run(query)

def get_full_schema():
    """
        Tool to extract Schema of the Data Base
    """
    tables = get_db().get_usable_table_names()
    schema = {}
    for table in tables:
        schema[table] = get_columns(table)
    return schema

def get_foreign_keys():
    """
        Tool to get all Foreign keys
    """
    query = """
    SELECT
        tc.table_name AS table,
        kcu.column_name AS column,
        ccu.table_name AS foreign_table,
        ccu.column_name AS foreign_column
    FROM 
        information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
    WHERE constraint_type = 'FOREIGN KEY';
    """
    return get_db().run(query)

def fetch_invoice_sample():
    query = """
    SELECT invoice_date, total
    FROM Invoice
    ORDER BY invoice_date DESC
    LIMIT 5
    """

    rows = get_db().run(query)

    if isinstance(rows, str):
        lines = rows.strip().split("\n")
        data = []
        for line in lines:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 2:
                data.append({
                    "invoice_date": parts[0],
                    "total": parts[1]
                })
        return data

    result = []
    for row in rows:
        if isinstance(row, (list, tuple)) and len(row) >= 2:
            result.append({
                "invoice_date": row[0],
                "total": row[1]
            })
    return result
