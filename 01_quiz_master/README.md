# Project 1: AI Quiz Master

An AI-powered quiz app that generates quizzes on **any topic** in seconds. Pick a topic, choose your difficulty, and test your knowledge!

## What It Does
- Enter any topic (Space, Cricket, Marvel, Python, History -- literally anything)
- AI generates multiple-choice questions instantly
- Take the quiz one question at a time
- Get your score with detailed explanations for every answer

## How to Run
```bash
# Make sure you've set up your .env file with your OpenAI API key
cd 01_quiz_master
streamlit run app.py
```

## Python Concepts You'll Learn
- Variables and data types (strings, integers, booleans)
- Lists and dictionaries
- Functions with parameters and return values
- if/elif/else conditionals
- For loops
- Working with APIs (OpenAI)
- JSON parsing
- Environment variables
- Building web apps with Streamlit

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Main Streamlit web app - the UI and quiz flow |
| `quiz_logic.py` | Generates quizzes using OpenAI, checks answers, calculates scores |
| `utils.py` | Helper functions for loading API keys |

## Tech Stack
- Python
- Streamlit (web interface)
- OpenAI API (quiz generation)
- python-dotenv (API key management)
