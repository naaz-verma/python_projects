# Project 11: AI Treasure Hunt

A grid-based treasure hunting game where an AI guide gives you cryptic clues to find hidden treasure. Navigate through different terrains, follow the warmth indicator, and find the gem in as few moves as possible!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else, strings)
- Completed the Python Starter course

---

## What Is This Project About?

A treasure has been hidden somewhere on a grid map. You start at a random position and must find it by moving North, South, East, or West. After each move, you get two things:

1. A **warmth indicator** (Burning Hot / Hot / Warm / Cool / Cold / Freezing) that tells you how close you are
2. An **AI-generated clue** that hints at the direction, written in a creative style based on your difficulty

The game uses an **emoji grid** to display the map with different terrains (grass, trees, mountains, water) and fog of war on harder difficulties.

**Features:**
- 3 difficulty levels (Easy: 6x6, Medium: 8x8, Hard: 10x10)
- Fog of war on Medium and Hard (you only see tiles you've visited)
- AI-generated clues that get more cryptic on harder difficulties
- Warmth indicator with color-coded display
- Star rating and scoring based on how efficiently you found the treasure

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

Shared Gemini API wrapper (same across all AI game projects).

### File 2: `game_map.py` -- The Map & Game Logic (Read This First)

**What it does:** Creates the game grid, handles movement, calculates distances, and generates AI clues.

**Key data:**
```python
# Terrain types with emoji mappings
TERRAIN = {
    "grass": "🟩",
    "tree": "🌲",
    "mountain": "⛰️",
    "water": "🌊",
    "fog": "⬜",
    "player": "🧭",
    "treasure": "💎",
}
```

**Key functions:**
```
create_grid()                --> Builds a 2D list with random terrain types
place_player_and_treasure()  --> Places player and treasure with minimum distance apart
calculate_distance()         --> Manhattan distance between two positions
get_direction_hint()         --> Returns "north", "south-east", etc.
get_warmth_level()           --> Converts distance to "Burning Hot", "Cold", etc.
move_player()                --> Updates position if move is valid (not off the grid)
render_grid()                --> Converts grid to list of emoji strings for display
generate_ai_clue()           --> Asks AI to write a creative directional clue
get_difficulty_settings()    --> Returns grid size and fog settings per difficulty
calculate_score()            --> Star rating based on moves vs optimal path
```

**Important Python you'll learn:**
```python
# 2D list (grid) creation
grid = [[random.choice(terrain_types) for _ in range(size)] for _ in range(size)]

# Manhattan distance
distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Direction calculation
if treasure is north-east of player:
    direction = "north-east"

# Set for tracking visited tiles
visited = set()
visited.add(tuple(player_pos))

# Emoji grid rendering
for row in range(size):
    row_emojis = []
    for col in range(size):
        if [row, col] == player_pos:
            row_emojis.append("🧭")
        elif fog_of_war and (row, col) not in visited:
            row_emojis.append("⬜")
        else:
            row_emojis.append(TERRAIN[grid[row][col]])
```

### File 3: `app.py` -- The Interface

**Layout:** Wide layout with two columns -- map on the left, clues on the right.

**Three screens:**
1. **Welcome** -- how to play, difficulty descriptions, terrain legend
2. **Gameplay** -- emoji grid, movement buttons (N/S/E/W), warmth indicator, AI clue panel
3. **Victory** -- star rating, score card, fully revealed map, clue history

**Key Streamlit concepts:**
- `st.columns([3, 2])` -- wider left column for the map
- `st.markdown(unsafe_allow_html=True)` -- renders emoji grid with custom CSS
- `st.toast()` -- shows a brief notification when hitting a wall
- `st.cache_resource` -- loads AI model once and reuses it
- Custom CSS classes for warmth colors (hot=red, cold=blue)

---

## How It Works

```
Player picks difficulty and starts a new hunt
        |
game_map.py creates:
   - A grid with random terrain
   - Player and treasure positions (minimum distance apart)
        |
Each move:
   - move_player() validates and updates position
   - calculate_distance() finds how far treasure is
   - get_warmth_level() converts distance to warmth text
   - generate_ai_clue() asks AI for a creative hint
   - render_grid() draws the emoji map (with fog if applicable)
        |
When player reaches treasure:
   - calculate_score() rates performance (1-5 stars)
   - Full map revealed, score card shown
```

---

## Terrain Legend

| Emoji | Meaning |
|-------|---------|
| 🧭 | Player (you) |
| 💎 | Treasure |
| 👣 | Visited tile |
| 🟩 | Grass |
| 🌲 | Tree |
| ⛰️ | Mountain |
| 🌊 | Water |
| ⬜ | Fog (hidden tile) |
| 🏠 | Starting position |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install streamlit python-dotenv requests` |
| API key error | Check `.env` file |
| Grid not displaying | Make sure your browser supports emoji rendering |
| Emojis look broken | Try a different browser (Chrome works best) |
| Can't move | You're at the edge of the map -- try a different direction |

---

## Python Concepts Used

| Concept | Where It's Used |
|---------|----------------|
| 2D Lists | Grid creation and terrain storage |
| Sets | Tracking visited tiles (`visited = set()`) |
| Tuples | Grid positions as `(row, col)` |
| Dictionaries | Terrain emoji mappings, difficulty settings, score data |
| Functions | Grid creation, movement, distance, clue generation |
| List comprehension | `[random.choice(...) for _ in range(size)]` |
| Math (abs) | Manhattan distance calculation |
| Random | Terrain generation, player/treasure placement |
| Session state | Tracking grid, position, moves, clues across reruns |
