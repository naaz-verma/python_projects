# Project 10: AI Word Duel

A creative word challenge game where players compete against AI judgment. Play solo to beat your high score, or challenge a friend in a 2-player duel!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else, strings)
- Completed the Python Starter course

---

## What Is This Project About?

Each round, the AI generates a unique **word challenge category** (like "A fruit that could be a superhero name" or "A word that sounds scary but means something nice"). Your goal is to come up with the most **creative** and **valid** answer possible. The AI judges your answer on creativity (1-10) and awards points based on your difficulty level.

**Features:**
- **Solo Challenge** -- play by yourself and chase a high score
- **2-Player Duel** -- compete head-to-head, same category, compare scores
- 3 difficulty levels with score multipliers (Easy: 1x, Medium: 1.5x, Hard: 2x)
- AI-generated categories that are different every time
- Rank titles based on your final score (Word Wizard, Vocabulary Master, etc.)

---

## Step-by-Step Setup

### Step 0: Check if Python is Installed

Open **Command Prompt** (search "cmd" in Start menu) and type:

```bash
python --version
```

You should see something like `Python 3.12.x`. If you get an error:
1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **IMPORTANT: Check the box "Add Python to PATH"** during installation
3. Restart your command prompt after installing

### Step 1: Install Required Packages

```bash
pip install streamlit
pip install python-dotenv
pip install requests
```

| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Turns our Python code into a web app |
| `python-dotenv` | Reads the API key from `.env` file |
| `requests` | Sends requests to the Gemini AI |

### Step 2: Get Your Gemini API Key (Free)

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"** and copy it

### Step 3: Create Your `.env` File

Create a file called `.env` in the project folder:

```
GEMINI_API_KEY=paste_your_key_here
```

### Step 4: Run the App

```bash
streamlit run app.py
```

Or: `python -m streamlit run app.py`

---

## Project Files -- What Each File Does

### File 1: `utils.py` -- The AI Connector

Connects to Google's Gemini AI. Same shared file used across all AI game projects.

### File 2: `word_game.py` -- The Game Logic

**What it does:** Generates word challenge categories, judges player answers, and calculates scores.

**Key functions:**
```
generate_category()      --> Asks AI to create a word challenge category with a hint
judge_answer()           --> AI evaluates if the answer is valid and scores creativity (1-10)
calculate_round_score()  --> Applies difficulty multiplier to creativity score
calculate_final_score()  --> Totals all round scores, counts valid answers, averages creativity
get_max_possible_score() --> Returns max achievable score for given rounds and difficulty
get_rank_title()         --> Converts score to a rank title (Word Wizard, etc.)
```

**Important Python you'll learn:**
```python
# AI prompt engineering -- telling the AI what format to respond in
prompt = f"""Generate a word challenge category...
Respond ONLY with valid JSON:
{{"category": "...", "hint": "..."}}"""

# JSON parsing
result = json.loads(text)

# Score calculation with multiplier
multipliers = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
score = int(creativity_score * multiplier)

# Rank system using thresholds
if ratio >= 0.9: return "Word Wizard"
elif ratio >= 0.7: return "Vocabulary Master"
```

### File 3: `app.py` -- The Interface

**Four screens:**
1. **Mode Selection** -- welcome, how-to-play, Solo vs Duel buttons
2. **Solo Play** -- category display, answer input, AI judgment with feedback
3. **Duel Play** -- player name entry, alternating turns with "look away" warnings, round results
4. **Game Over** -- final rank, score breakdown, round-by-round expanders

**Key Streamlit concepts:**
- `st.radio()` -- difficulty selector
- `st.slider()` -- number of rounds
- `st.chat_input()` is NOT used here -- uses `st.text_input()` instead
- `st.metric()` -- displays creativity score and points
- `st.expander()` -- collapsible round details in results
- `st.columns()` -- side-by-side display for duel mode

---

## How It Works

```
Player picks Solo or Duel mode
        |
Each round:
   - generate_category() asks AI for a creative category + hint
   - Player(s) type their answer
   - judge_answer() asks AI: "Is this valid? How creative (1-10)?"
   - calculate_round_score() applies difficulty multiplier
   - Show feedback and running total
        |
After all rounds:
   - calculate_final_score() totals everything up
   - get_rank_title() assigns a rank based on performance
   - Show breakdown with per-round details
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install streamlit python-dotenv requests` |
| API key error | Check `.env` file has `GEMINI_API_KEY=your_key` |
| AI not responding | Check internet connection |
| Scores seem unfair | The AI judges creativity -- try more unique answers! |

---

## Python Concepts Used

| Concept | Where It's Used |
|---------|----------------|
| Dictionaries | Category data, judgment results, round history |
| Lists | Storing round results for each player |
| Functions | `generate_category()`, `judge_answer()`, `calculate_round_score()` |
| f-strings | Dynamic prompts and display text |
| if/elif/else | Score multipliers, rank titles, game flow |
| JSON parsing | Converting AI responses to Python dicts |
| Session state | Tracking rounds, scores, and game phase |
| Math operations | Score multipliers, averages, max calculations |
