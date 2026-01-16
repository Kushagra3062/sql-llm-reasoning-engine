from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
import urllib

def connect_db():
    
    user = "postgres"
    password = urllib.parse.quote_plus("Codeis@04") 
    host = "localhost"
    port = "5432"
    dbname = "chinook_serial"

    pg_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    db = SQLDatabase.from_uri(pg_uri)
    return db