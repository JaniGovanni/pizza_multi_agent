from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

GroqLLM = ChatGroq(model="llama-3.1-70b-versatile", streaming=True)