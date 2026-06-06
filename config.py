# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL ="llama-3.3-70b-versatile"
    
    # Vector Store Configuration
    VECTOR_STORE_PATH = "./data/faiss_index"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # Database Configuration
    DATABASE_PATH = "./data/campus_chatbot.db"
    
    # Web Scraping Configuration
    SCRAPE_TIMEOUT = 10
    MAX_PAGES_SCRAPE = 50
    
    # Campus URLs (Configure these)
    CAMPUS_WEBSITE = os.getenv("CAMPUS_WEBSITE", "https://kakatiya.ac.in/")
    EVENTS_CALENDAR_URL = os.getenv("EVENTS_CALENDAR_URL", "https://kakatiya.ac.in/")
    PLACEMENTS_URL = os.getenv("PLACEMENTS_URL", "http://kucet.ac.in/placements")
    
    # Streamlit Configuration
    STREAMLIT_THEME = "light"
    MAX_HISTORY_ITEMS = 50
    
    # System Prompts
    SYSTEM_PROMPT = """You are a friendly and helpful campus information assistant for [Kakatiya University College of Engineering and Technology]. 
    You have access to comprehensive campus information including:
    - Academic policies and rules
    - Event schedules and activities
    - Club and organization details
    - Facility locations and hours
    - Placement and career information
    - Student procedures and processes
    
    Always be accurate, helpful, and direct users to official contacts when needed.
    If you don't know something, admit it and suggest they contact the relevant office."""