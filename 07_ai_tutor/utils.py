import os
import requests
from dotenv import load_dotenv


def load_api_key():
    """Load Gemini API key from .env file."""
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        return None
    return api_key


def get_gemini_model():
    """Return a simple wrapper that calls Gemini REST API."""
    api_key = load_api_key()
    if not api_key:
        return None
    return GeminiModel(api_key)


class GeminiModel:
    """Lightweight wrapper around Gemini REST API."""

    def __init__(self, api_key, model="gemma-3-4b-it"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate_content(self, prompt):
        """Generate content from a text prompt."""
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        r = requests.post(url, json=data, timeout=60, verify=False)
        r.raise_for_status()
        return GeminiResponse(r.json())

    def start_chat(self, history=None):
        """Return a chat session."""
        return GeminiChat(self)


class GeminiChat:
    """Simple multi-turn chat using Gemini REST API."""

    def __init__(self, model):
        self.model = model
        self.history = []

    def send_message(self, message):
        """Send a message and get a response."""
        self.history.append({"role": "user", "parts": [{"text": message}]})
        url = f"{self.model.base_url}/models/{self.model.model}:generateContent?key={self.model.api_key}"
        data = {"contents": self.history}
        r = requests.post(url, json=data, timeout=60, verify=False)
        r.raise_for_status()
        resp = r.json()
        text = resp["candidates"][0]["content"]["parts"][0]["text"]
        self.history.append({"role": "model", "parts": [{"text": text}]})
        return GeminiResponse(resp)


class GeminiResponse:
    """Simple response wrapper."""

    def __init__(self, data):
        self._data = data
        self.text = data["candidates"][0]["content"]["parts"][0]["text"]
