from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
import urllib
from contextvars import ContextVar

# Global context variable to hold the database connection for the current request
db_context: ContextVar[SQLDatabase] = ContextVar("db_context", default=None)

def get_db() -> SQLDatabase:
    """
    Retrieves the database connection for the current context.
    Falls back to a default connection if no context is set (useful for testing/defaults).
    """
    db = db_context.get()
    if db is None:
        # Fallback to default (Chinook) if no specific DB is set in context
        # This ensures existing tests or default behavior still works
        print("[DB] No context found, creating default connection.")
        return create_default_connection()
    return db

def set_db(db: SQLDatabase):
    """Sets the database connection for the current context."""
    db_context.set(db)

def create_default_connection() -> SQLDatabase:
    """Creates the default connection to the Chinook database."""
    user = "postgres"
    password = urllib.parse.quote_plus("admin") 
    host = "localhost"
    port = "5432"
    dbname = "chinook"

    pg_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return SQLDatabase.from_uri(pg_uri)

def connect_db():
    """
    Legacy/Wrapper function to maintain compatibility.
    Now simply calls get_db().
    """
    return get_db()