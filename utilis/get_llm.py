from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile")
    except:
        print("Error Loading Model")
        return
    return llm

def get_llm_llama():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    except:
        print("Error Loading Model")
        return
    return llm