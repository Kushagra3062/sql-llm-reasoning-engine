from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
import urllib.parse
from contextvars import ContextVar

load_dotenv()

# Global context variable to hold the database connection for the current request
db_context: ContextVar[SQLDatabase] = ContextVar("db_context", default=None)

def get_db() -> SQLDatabase:
    """
    Retrieves the database connection for the current context.
    Falls back to a default connection if no context is set.
    """
    db = db_context.get()
    if db is None:
        return create_default_connection()
    return db

def set_db(db: SQLDatabase):
    """Sets the database connection for the current context."""
    db_context.set(db)

def create_default_connection() -> SQLDatabase:
    """Creates the connection using DATABASE_URL env var or fallback to local market_db."""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        # Fallback to local development settings
        user = "postgres"
        password = urllib.parse.quote_plus("admin") 
        host = "localhost"
        port = "5432"
        dbname = "market_db"
        db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        print(f"[DB] Using local fallback connection: {host}:{port}/{dbname}")
    else:
        print("[DB] Using DATABASE_URL from environment.")
        
    return SQLDatabase.from_uri(db_url)

def connect_db():
    return get_db()