from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
def get_llm():
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    try:
        llm = ChatGroq(model="openai/gpt-oss-120b")
    except:
        print("Error Loading Model")
        return
    return llm

def get_llm_llama():
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    except:
        print("Error Loading Model")
        return
    return llm