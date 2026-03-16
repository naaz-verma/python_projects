# Project 6: AI Chatbot with Personality

An AI chatbot that takes on different personalities -- chat with a pirate, a Shakespearean poet, a sarcastic comedian, or create your own custom persona!

## What It Does
- Choose from pre-built personality profiles (Pirate, Poet, Comedian, Scientist, Motivational Coach)
- Create your own custom personality
- Natural back-and-forth conversation with context memory
- Personality stays consistent throughout the conversation
- Export chat history

## How to Run
```bash
# Make sure you've set up your .env file with your OpenAI API key
cd 06_ai_chatbot
streamlit run app.py
```

## Python Concepts You'll Learn
- Dictionaries (personality configs)
- Lists (chat history management)
- String formatting (system prompts)
- API integration (OpenAI chat completions)
- Session state (conversation memory)
- Streamlit chat interface

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Streamlit chat interface with personality selector |
| `chatbot.py` | Chatbot engine with personality management |
| `personalities.py` | Pre-built personality definitions |
| `utils.py` | API key loading utilities |

## Tech Stack
- Python
- Streamlit (chat interface)
- OpenAI API (conversation)
- python-dotenv (API key management)
