# Project 12: AI Detective

An interactive murder mystery game where you interrogate AI-powered suspects, examine evidence, and solve the case. Each suspect is role-played by AI with their own personality, alibi, and secrets!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else, strings)
- Completed the Python Starter course

---

## What Is This Project About?

You play as a detective investigating a crime. The AI generates a complete mystery case with a victim, 4 suspects, physical evidence, and a hidden culprit. Your job:

1. **Examine the crime scene** -- learn about the victim, weapon, and circumstances
2. **Interrogate suspects** -- chat with AI-powered suspects who stay in character (the guilty one shows subtle nervousness!)
3. **Examine evidence** -- reveal clues one at a time that point to the culprit
4. **Take notes** -- keep track of inconsistencies and observations
5. **Make your accusation** -- name the suspect you think did it

**Features:**
- 4 case types (Mansion Mystery, Office Crime, Campus Case, Hotel Heist)
- AI generates unique cases every time with different suspects, motives, and clues
- Each suspect is a separate AI chat session with their own personality
- The guilty suspect shows subtle nervousness and has alibi inconsistencies
- Progressive evidence reveal system
- Built-in notebook for taking notes
- Full case breakdown after solving

---

## Step-by-Step Setup

### Step 0: Check if Python is Installed

```bash
python --version
```

### Step 1: Install Required Packages

```bash
pip install streamlit
pip install python-dotenv
pip install requests
```

| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Web app framework |
| `python-dotenv` | Reads API key from `.env` file |
| `requests` | Sends requests to Gemini AI |

### Step 2: Get Your Gemini API Key (Free)

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in and click **"Create API Key"**

### Step 3: Create Your `.env` File

```
GEMINI_API_KEY=paste_your_key_here
```

### Step 4: Run the App

```bash
streamlit run app.py
```

---

## Project Files -- What Each File Does

### File 1: `utils.py` -- The AI Connector

Shared Gemini API wrapper. This file is the same across all AI game projects. It has:
- `GeminiModel` -- sends single prompts to the AI
- `GeminiChat` -- manages multi-turn conversations (used for interrogation!)
- `GeminiResponse` -- wraps the AI response

### File 2: `case_generator.py` -- The Mystery Builder (Read This First)

**What it does:** Generates complete mystery cases and manages suspect interactions.

**Key data:**
```python
# Available case settings
CASE_TYPES = {
    "Mansion Mystery": "a wealthy family's countryside mansion during a dinner party",
    "Office Crime": "a corporate office building after hours",
    "Campus Case": "a university campus during exam week",
    "Hotel Heist": "a luxury hotel during a gala event",
}
```

**Key functions:**
```
generate_case()        --> Asks AI to create a full case (victim, suspects, clues, solution)
get_suspect_prompt()   --> Creates a "system prompt" that tells AI how to role-play as a suspect
get_guilty_suspect()   --> Finds which suspect has is_guilty: true
check_accusation()     --> Compares player's accusation against the real culprit
get_fallback_case()    --> Pre-built case if AI generation fails
```

**Important Python you'll learn:**
```python
# Complex JSON prompt engineering
prompt = f"""Create a murder mystery with EXACTLY this JSON structure:
{{
    "title": "A catchy case title",
    "victim": {{"name": "...", "role": "..."}},
    "suspects": [
        {{"name": "...", "alibi": "...", "is_guilty": false}},
        ...
    ],
    "clues": ["Clue 1", "Clue 2", "Clue 3"],
    "solution": "..."
}}"""

# Role-play prompt for guilty vs innocent suspects
if suspect.get("is_guilty"):
    note = "You ARE guilty but must NOT confess directly..."
else:
    note = "You are INNOCENT. Answer honestly..."

# Fuzzy name matching for accusations
correct = accused_lower == guilty_lower or accused_lower in guilty_lower

# Validation with fallback
if len(case["suspects"]) != 4:
    return get_fallback_case()
```

### File 3: `app.py` -- The Interface (Read This Last)

**Five tabs:**
1. **Crime Scene** -- victim info, crime details, suspect overview
2. **Interrogation** -- select a suspect, chat with them using `st.chat_message`
3. **Evidence** -- reveal clues one at a time with "Examine Evidence" button
4. **Notebook** -- auto-populated notes + custom note-taking
5. **Make Accusation** -- select suspect, explain reasoning, submit

**Key Streamlit concepts:**
- `st.tabs()` -- creates the 5-tab investigation interface
- `st.chat_message()` -- displays conversation bubbles for interrogation
- `st.chat_input()` -- the text box at the bottom for asking questions
- `st.session_state` -- tracks interview history, clues revealed, notebook entries
- `st.progress()` -- shows investigation progress in sidebar
- `st.expander()` -- collapsible suspect details in the solved screen

**Multi-turn chat:**
```python
# Each suspect gets their own chat session
chat = model.start_chat()
# First message is the "system prompt" (defines their character)
chat.send_message(get_suspect_prompt(suspect, case))
# Then each player question continues the conversation
response = chat.send_message(user_question)
```

---

## How It Works

```
Player picks a case type and clicks "Generate New Case"
        |
generate_case() asks AI to create:
   - Victim details (name, role, description)
   - Crime details (weapon, location, time, discovery)
   - 4 suspects (1 guilty, 3 innocent) with alibis and motives
   - 3 clues pointing to the guilty suspect
   - The solution
        |
Investigation phase:
   - Crime Scene tab: read the case details
   - Interrogation tab: chat with each suspect (AI role-plays each one)
   - Evidence tab: reveal clues one at a time
   - Notebook tab: track findings
        |
When player makes accusation:
   - check_accusation() compares against the real culprit
   - Full case breakdown revealed
   - Investigation stats shown (suspects interviewed, clues found)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install streamlit python-dotenv requests` |
| API key error | Check `.env` file |
| Case not generating | The AI needs a moment -- wait for the spinner |
| Suspect not responding | Check internet connection |
| Chat history disappearing | Each suspect's chat is stored separately in session state |

---

## Python Concepts Used

| Concept | Where It's Used |
|---------|----------------|
| Dictionaries | Case data (nested dicts for victim, crime, suspects) |
| Lists | Suspects list, clues list, notebook entries |
| Sets | `suspects_interviewed` -- tracking which suspects were questioned |
| Functions | `generate_case()`, `get_suspect_prompt()`, `check_accusation()` |
| String formatting | Complex f-string prompts for AI |
| JSON parsing | Parsing AI-generated case from JSON text |
| Boolean logic | `is_guilty` flag, fuzzy name matching |
| Multi-turn chat | `GeminiChat` class with conversation history |
| Session state | Separate chat sessions per suspect, persistent notebook |
| Error handling | try/except with fallback case if AI fails |
