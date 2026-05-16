# Project 13: AI Emoji Story Battle

A creative game with two modes: write stories from emojis, or pick emojis for stories. The AI judges your creativity, coherence, and emoji usage across multiple rounds!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else, strings)
- Completed the Python Starter course

---

## What Is This Project About?

This game has two modes:

### Mode 1: Emoji to Story
The AI gives you **5 random emojis** from different categories. You write a **short story** (2-5 sentences) that weaves all 5 emojis into a narrative. The AI scores you on:
- **Creativity** (1-10) -- how imaginative is your story?
- **Coherence** (1-10) -- does it make sense as a narrative?
- **Emoji Usage** (1-10) -- did you naturally incorporate all 5 emojis?

### Mode 2: Story to Emoji
The AI generates a vivid **scenario** (e.g., "A brave knight rides through a thunderstorm to rescue a princess"). You pick **exactly 5 emojis** from a grid that best represent the scenario. The AI scores you on:
- **Relevance** (1-10) -- how well do the emojis match?
- **Creativity** (1-10) -- how clever are your choices?
- **Coverage** (1-10) -- do the emojis cover all parts of the scenario?

**Features:**
- 72 emojis across 6 categories (animals, food, weather, emotions, objects, places)
- 3-5 rounds per game with running score
- Star rating system (1-5 stars based on average score)
- Detailed round-by-round breakdown at the end

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

Shared Gemini API wrapper (same across all AI game projects).

### File 2: `emoji_game.py` -- The Game Logic (Read This First)

**What it does:** Manages emoji sets, scoring, scenario generation, and all game logic.

**Key data:**
```python
# 72 emojis in 6 categories
EMOJI_SETS = {
    "animals": ["🐶", "🐱", "🐼", "🦁", "🐸", "🦊", "🐧", "🦋", "🐙", "🦄", "🐝", "🐬"],
    "food":    ["🍕", "🍩", "🌮", "🍦", "🎂", "🍣", "🥑", "🍔", "🍪", "🧁", "🍉", "🥐"],
    "weather": ["☀️", "🌧️", "⛈️", "🌈", "❄️", "🌪️", "🌙", "⭐", "🔥", "💨", "🌊", "☁️"],
    "emotions":["😊", "😢", "😡", "😱", "🥳", "😴", "🤔", "😎", "🥺", "😂", "💀", "🤯"],
    "objects": ["🔑", "💡", "🎸", "📱", "⏰", "🎯", "🧲", "🔮", "🗡️", "🛡️", "💎", "🏆"],
    "places":  ["🏠", "🏔️", "🏖️", "🌋", "🏰", "🚀", "🎪", "🏥", "🏫", "⛩️", "🗽", "🎡"],
}
```

**Key functions:**
```
get_random_emojis()       --> Picks 5 emojis from different categories for variety
score_story()             --> AI scores a player's story (creativity, coherence, emoji_usage)
generate_scenario()       --> AI creates a vivid 2-3 sentence scenario
judge_emoji_match()       --> AI scores emoji selection (relevance, creativity, coverage)
get_all_emojis_flat()     --> Returns all 72 emojis as a flat list
calculate_final_stats()   --> Computes total, average, best round from all rounds
get_star_rating()         --> Converts score to star emoji string (⭐⭐⭐⭐⭐)
```

**Important Python you'll learn:**
```python
# Picking from different categories for variety
random.shuffle(categories)
for i in range(count):
    cat = categories[i % len(categories)]
    emoji = random.choice(EMOJI_SETS[cat])

# AI scoring with JSON response
prompt = f"""Score the story on 3 criteria (each 1-10):
1. creativity: How creative is the story?
2. coherence: Does it make sense?
3. emoji_usage: How well were all 5 emojis used?
Respond ONLY with valid JSON: {{"creativity": 7, "coherence": 8, ...}}"""

# Clamping scores to valid range
result[key] = max(1, min(10, int(result.get(key, 5))))

# Star rating from ratio
ratio = score / max_score
if ratio >= 0.9: return "⭐⭐⭐⭐⭐"
elif ratio >= 0.7: return "⭐⭐⭐⭐"

# Flat list from nested dict
all_emojis = []
for cat_emojis in EMOJI_SETS.values():
    all_emojis.extend(cat_emojis)
```

### File 3: `app.py` -- The Interface

**Three screens:**
1. **Welcome** -- mode descriptions, Start Game button
2. **Playing** -- Mode A shows emojis + text area; Mode B shows scenario + emoji grid picker
3. **Game Over** -- final stats, star rating, round-by-round expanders

**Key Streamlit concepts:**
- `st.radio()` -- game mode selector in sidebar
- `st.slider()` -- number of rounds (3-5)
- `st.text_area()` -- story input for Emoji-to-Story mode
- `st.button()` -- emoji picker grid (click to select/deselect)
- `st.metric()` -- score display per criteria
- `st.progress()` -- round progress bar
- `st.markdown(unsafe_allow_html=True)` -- large emoji display with custom styling

**Emoji picker grid:**
```python
# Each category is a row of clickable buttons
for category, emojis in EMOJI_SETS.items():
    cols = st.columns(len(emojis))
    for idx, emoji in enumerate(emojis):
        with cols[idx]:
            if st.button(emoji, ...):
                # Toggle selection
                if emoji in selected:
                    selected.remove(emoji)
                elif len(selected) < 5:
                    selected.append(emoji)
```

---

## How It Works

```
Player picks mode (Emoji-to-Story or Story-to-Emoji)
        |
Mode A (Emoji to Story):              Mode B (Story to Emoji):
   get_random_emojis(5)                  generate_scenario() via AI
   Player writes a story                 Player picks 5 emojis from grid
   score_story() via AI                  judge_emoji_match() via AI
        |                                       |
        +----------- After each round ----------+
        |
   Show score (3 criteria, each /10)
   Show star rating and AI feedback
        |
After all rounds:
   calculate_final_stats()
   Show total, average, best round, overall stars
   Expandable round-by-round breakdown
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install streamlit python-dotenv requests` |
| API key error | Check `.env` file |
| Emojis not showing | Use Chrome -- it has the best emoji support |
| AI gives low scores | Try incorporating ALL 5 emojis naturally into your story |
| Emoji buttons hard to click | They're small on purpose -- try zooming in |

---

## Python Concepts Used

| Concept | Where It's Used |
|---------|----------------|
| Dictionaries | Emoji categories, score results, round history |
| Lists | Emoji arrays, selected emojis, rounds history |
| Functions | `get_random_emojis()`, `score_story()`, `judge_emoji_match()` |
| Modulo operator | `categories[i % len(categories)]` for cycling through categories |
| `max()` / `min()` | Clamping scores: `max(1, min(10, score))` |
| `random.shuffle()` | Randomizing category order for variety |
| `random.choice()` | Picking a random emoji from a category |
| JSON parsing | Converting AI score responses to Python dicts |
| String joining | `" ".join(emojis)` for display |
| Session state | Tracking selected emojis, round history, scores |
