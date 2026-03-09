
import psycopg2
import sys
import os

# New Supabase URL from user
DEST_URL = "postgresql://postgres:Kushagra%403062@db.yzndnwachkjjvuwzlxqv.supabase.co:5432/postgres"
DUMP_FILE = "market_db.sql"

def import_dump():
    if not os.path.exists(DUMP_FILE):
        print(f"Error: {DUMP_FILE} not found.")
        return

    try:
        print(f"Connecting to Supabase...")
        conn = psycopg2.connect(DEST_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print(f"Reading {DUMP_FILE}...")
        with open(DUMP_FILE, 'r', encoding='utf-8') as f:
            sql = f.read()
            
        print("Executing SQL dump (this may take a minute)...")
        # Executing as one big string might fail for huge files, 
        # but let's try it first for this market_db dump.
        try:
            cur.execute(sql)
            print("SUCCESS: Dump imported to Supabase.")
        except Exception as e:
            print(f"Partial Failure or Error: {e}")
            print("Trying to split by semicolon and execute (fallback)...")
            conn.rollback()
            conn.autocommit = True
            # Simple splitter (might fail on semicolons in strings/functions)
            for statement in sql.split(';'):
                if statement.strip():
                    try:
                        cur.execute(statement)
                    except Exception as e2:
                        print(f"Error in statement: {e2}")
            print("Fallback execution finished.")
            
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import_dump()
