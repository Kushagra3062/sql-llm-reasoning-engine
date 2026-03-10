from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    
    os.environ["GROQ_API_KEY"] = groq_api_key
    # Default model for most agents
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

def get_llm_llama():
    return get_llm()
