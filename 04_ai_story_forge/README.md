# Project 4: AI Story Forge

A choose-your-own-adventure game powered by AI. The AI writes the story, you make the decisions, and AI generates artwork for key scenes.

## What It Does
- Pick a genre (Fantasy, Sci-Fi, Horror, Mystery, Adventure)
- AI writes an immersive opening scene
- Make choices at every turn -- the story adapts to YOUR decisions
- AI generates images for key story moments
- Save and revisit your story history

## How to Run
```bash
# Make sure you've set up your .env file with your OpenAI API key
cd 04_ai_story_forge
streamlit run app.py
```

## Python Concepts You'll Learn
- Classes with state management (StoryEngine)
- Prompt engineering for creative AI
- Multi-API integration (text + image generation)
- Session state and conversation history
- Error handling and retry logic
- Working with binary data (images)

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Streamlit interface for the interactive story |
| `story_engine.py` | Manages story state, generates narrative and choices |
| `image_gen.py` | Generates scene artwork using OpenAI DALL-E |

## Tech Stack
- Python
- Streamlit (web interface)
- OpenAI GPT (story generation)
- OpenAI DALL-E (image generation)
- python-dotenv (API key management)
