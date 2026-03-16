import os
from openai import OpenAI
from dotenv import load_dotenv


def load_api_key():
    """Load OpenAI API key from .env file."""
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-api-key-here":
        return None
    return api_key


def get_openai_client():
    """Create and return an OpenAI client."""
    api_key = load_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)
