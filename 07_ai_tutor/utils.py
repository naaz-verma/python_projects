import os
import google.generativeai as genai
from dotenv import load_dotenv


def load_api_key():
    """Load Gemini API key from .env file."""
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        return None
    return api_key


def get_gemini_model():
    """Configure Gemini and return a GenerativeModel instance."""
    api_key = load_api_key()
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")
