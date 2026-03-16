# Project 7: AI Tutor

An intelligent tutoring assistant that helps students learn any subject using the Socratic method -- guiding them to answers instead of just giving them away.

## What It Does
- Pick a subject (Math, Science, History, Programming, English, or any custom topic)
- Choose your level (Beginner, Intermediate, Advanced)
- Ask questions and get guided explanations
- AI uses Socratic method -- asks questions to help you think
- Get practice problems with step-by-step hints
- Track what you've learned in the session

## How to Run
```bash
# Make sure you've set up your .env file with your OpenAI API key
cd 07_ai_tutor
streamlit run app.py
```

## Python Concepts You'll Learn
- Prompt engineering for educational AI
- State management across interactions
- Structured data handling (topics, levels, progress)
- API integration with conversation context
- Building interactive educational interfaces

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Streamlit interface for the tutoring experience |
| `tutor_engine.py` | AI tutor logic with Socratic method prompting |
| `subjects.py` | Subject configurations and curriculum outlines |
| `utils.py` | API key loading utilities |

## Tech Stack
- Python
- Streamlit (interface)
- OpenAI API (tutoring intelligence)
- python-dotenv (API key management)
