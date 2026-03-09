
import psycopg2
import sys

# Source: Local market_db
# Destination: Supabase

SOURCE_URL = "postgresql://postgres:admin@localhost:5432/market_db"
DEST_URL = "postgresql://postgres:Kushagra%403062@db.nxgdxwwiwapdmikhnblz.supabase.co:5432/postgres"

TABLES = ["companies", "financial_statements", "metadata_versions", "market_prices"]

def migrate():
    try:
        source_conn = psycopg2.connect(SOURCE_URL)
        dest_conn = psycopg2.connect(DEST_URL)
        
        source_cur = source_conn.cursor()
        dest_cur = dest_conn.cursor()
        
        print("Connected to both databases.")
        
        for table in TABLES:
            print(f"Migrating table: {table}...")
            
            # Get columns
            source_cur.execute(f"SELECT * FROM {table} LIMIT 0")
            cols = [desc[0] for desc in source_cur.description]
            col_list = ", ".join(cols)
            placeholders = ", ".join(["%s"] * len(cols))
            
            # Create table structure (simplified)
            # In a real scenario, you'd use pg_dump, but here we assume schema might exist or we just need data
            # Supabase usually has a 'public' schema.
            
            # Fetch all data
            source_cur.execute(f"SELECT * FROM {table}")
            rows = source_cur.fetchall()
            
            print(f"  Found {len(rows)} rows. Inserting...")
            
            # Truncate if exists or just try insert
            try:
                dest_cur.execute(f"TRUNCATE TABLE {table} CASCADE")
            except:
                dest_conn.rollback()
                dest_cur = dest_conn.cursor()

            insert_query = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"
            dest_cur.executemany(insert_query, rows)
            dest_conn.commit()
            print(f"  Successfully migrated {table}.")
            
        source_conn.close()
        dest_conn.close()
        print("\nMigration COMPLETED successfully!")
        
    except Exception as e:
        print(f"\nERROR during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
