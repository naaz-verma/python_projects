# Project 1: AI Quiz Master

An AI-powered quiz app that generates quizzes on **any topic** in seconds. Pick a topic, choose your difficulty, and test your knowledge!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else)

---

## Step-by-Step Setup (Fresh Laptop)

### Step 0: Check if Python is Installed

Open **Command Prompt** (search "cmd" in Start menu) and type:

```bash
python --version
```

You should see something like `Python 3.12.x`. If you get an error:
1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **IMPORTANT: Check the box "Add Python to PATH"** during installation
3. Restart your command prompt after installing

Also verify pip (Python's package installer) is available:

```bash
pip --version
```

If `pip` gives an error, try `python -m pip --version` instead.

### Step 1: Install VS Code (if not installed)

1. Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Install with default settings
3. Open VS Code
4. Install the **Python extension**: click Extensions icon (left sidebar) > search "Python" > install the one by Microsoft

### Step 2: Open the Project Folder

1. In VS Code: **File > Open Folder** > navigate to `01_quiz_master` folder
2. Open the terminal: **Terminal > New Terminal** (or press `` Ctrl + ` ``)
3. Make sure the terminal shows you're inside the project folder

### Step 3: Install Required Packages

Run these commands **one by one** in the VS Code terminal:

```bash
pip install streamlit
pip install python-dotenv
pip install requests
```

If `pip` doesn't work, try with `python -m pip` instead:
```bash
python -m pip install streamlit
python -m pip install python-dotenv
python -m pip install requests
```

**What each package does:**
| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Turns our Python code into a web app (no HTML/CSS needed) |
| `python-dotenv` | Reads our secret API key from a `.env` file safely |
| `requests` | Sends HTTP requests to the Gemini API (like a browser but in code) |

**Note:** These are NOT built into Python. Python comes with only basic stuff (like `os`, `json`, `math`). For anything extra, we install packages using `pip` — Python's package manager. Think of it like an app store for Python libraries.

### Step 4: Get Your Gemini API Key (Free)

**What is an API key?** It's like a password that lets your code talk to Google's AI. Without it, Google won't respond to your requests.

1. Go to [https://aistudio.google.com/apikey](httvvcccbkbkdlhgvvhdvjtftikdrrjrups://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (it looks like `AIzaSy...`)
5. Keep this key private — don't share it with anyone

### Step 5: Create the `.env` File

In the **parent folder** (the folder that CONTAINS 01_quiz_master, not inside it), create a new file called `.env`:

```
GEMINI_API_KEY=paste-your-key-here
```

**How to create it:**
1. In VS Code, right-click in the parent folder > New File
2. Name it exactly `.env` (yes, it starts with a dot, no extension)
3. Type the line above, replacing `paste-your-key-here` with your actual key
4. Save the file (Ctrl+S)

**Rules:**
- No quotes around the key
- No spaces around the `=` sign
- Never share this file or push it to GitHub

**Folder structure should look like:**
```
python_projects/          <-- .env file goes HERE
    .env
    01_quiz_master/
        app.py
        quiz_logic.py
        utils.py
```

### Step 6: Run the App

From the terminal, make sure you're inside the `01_quiz_master` folder, then run:

```bash
streamlit run app.py
```

If that doesn't work, try:
```bash
python -m streamlit run app.py
```

This will automatically open your browser at `http://localhost:8501` with the quiz app running.

To **stop the app**: press `Ctrl+C` in the terminal.

---

## Project Files — What Each File Does

Read the files in this order when learning:

### File 1: `utils.py` — The Helper (Read This First)

**What it does:** Loads your API key and talks to Gemini.

**Key concepts for students:**
- `os.getenv()` — reads a value from environment variables
- `load_dotenv()` — loads the `.env` file so `os.getenv` can find our key
- `requests.post()` — sends data to a URL (the Gemini API) and gets a response
- The file has classes (GeminiModel, GeminiChat, GeminiResponse) — **you don't need to understand classes yet**. Just know that `get_gemini_model()` gives you an object that can call `generate_content(prompt)` and it returns AI-generated text.

**The only function students need to understand:**
```python
def load_api_key():
    load_dotenv(...)              # Load .env file
    api_key = os.getenv("GEMINI_API_KEY")  # Get the key
    return api_key               # Return it
```

### File 2: `quiz_logic.py` — The Brain (Read This Second)

**What it does:** Creates the quiz using AI and checks answers.

**Key concepts for students:**
- Writing a **prompt** (a text instruction for the AI)
- Asking AI to respond in **JSON format** (structured data)
- `json.loads()` — converts a JSON string into a Python dictionary
- Simple functions: `check_answer()` and `calculate_score()`

**Three functions, all simple:**
```
generate_quiz()    → sends a prompt to Gemini, gets back questions as JSON
check_answer()     → compares two strings (user answer vs correct answer)
calculate_score()  → loops through answers, counts correct ones
```

### File 3: `app.py` — The Face (Read This Last)

**What it does:** The web interface using Streamlit.

**Key concepts for students:**
- `st.text_input()` — creates a text box on the web page
- `st.button()` — creates a clickable button
- `st.radio()` — creates radio button options
- `st.columns()` — splits the page into columns
- `st.session_state` — remembers data between button clicks (like a dictionary that persists)

---

## Teaching Flow (Recommended Order)

```
Step 1: Setup          →  Install packages, create .env, get API key
Step 2: utils.py       →  Explain API keys, environment variables, how we talk to AI
Step 3: quiz_logic.py  →  Explain prompts, JSON, how AI generates a quiz
Step 4: app.py         →  Explain Streamlit basics, session state, the UI
Step 5: Run it!        →  streamlit run app.py — see it work
Step 6: Experiment     →  Change the prompt, add more options, try different topics
```

---

## How It Works (Simple Explanation)

```
User types "Space" as topic
        ↓
app.py sends topic to quiz_logic.py
        ↓
quiz_logic.py builds a prompt:
   "Generate 5 questions about Space in JSON format..."
        ↓
utils.py sends this prompt to Google Gemini API
        ↓
Gemini returns JSON with questions, options, answers
        ↓
quiz_logic.py parses the JSON into a Python list of dictionaries
        ↓
app.py shows questions one by one using Streamlit
        ↓
User answers → calculate_score() counts correct answers
        ↓
App shows score + explanations
```

---

## Quick Reference: All Terminal Commands

```bash
# ---- First time setup (run ONCE) ----

# Check Python is installed
python --version

# Check pip is installed
pip --version

# Install all required packages
pip install streamlit
pip install python-dotenv
pip install requests

# ---- Every time you want to run the app ----

# Navigate to project folder (if not already there)
cd 01_quiz_master

# Start the app
streamlit run app.py

# OR if streamlit command not found:
python -m streamlit run app.py

# Stop the app: press Ctrl+C in terminal

# ---- Useful checks ----

# See all installed packages
pip list

# Check if a specific package is installed
pip show streamlit
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install streamlit` |
| `ModuleNotFoundError: No module named 'dotenv'` | Run `pip install python-dotenv` (NOT `pip install dotenv`) |
| `Gemini API key not found!` | Make sure `.env` file exists in the parent folder with `GEMINI_API_KEY=your-key` |
| `streamlit: command not found` | Try `python -m streamlit run app.py` |
| `'python' is not recognized` | Python not installed or not in PATH. Reinstall Python and check "Add to PATH" |
| `pip: command not found` | Try `python -m pip install ...` instead of `pip install ...` |
| App opens but quiz generation fails | Check your API key is valid at [aistudio.google.com](https://aistudio.google.com) |
| `requests.exceptions.SSLError` | Your network may block API calls. Try a different network or mobile hotspot |
| Browser doesn't open automatically | Manually go to `http://localhost:8501` in your browser |
| `.env` file not working | Make sure the file is in the parent folder, not inside 01_quiz_master |

---

## Python Concepts Used in This Project

| Concept | Where It's Used |
|---------|----------------|
| Variables & strings | Everywhere — topic, difficulty, API key |
| Lists | Storing questions, user answers |
| Dictionaries | Each question is a dict with keys: question, options, correct, explanation |
| Functions | `generate_quiz()`, `check_answer()`, `calculate_score()`, `load_api_key()` |
| f-strings | Building the prompt: `f"Generate {num_questions} questions about {topic}"` |
| for loops | Looping through questions, calculating scores |
| if/elif/else | Checking answers, showing grades |
| json.loads() | Converting API response text into Python data |
| Environment variables | Keeping the API key secret via `.env` |

**Concepts NOT needed:** Classes/OOP (utils.py has classes but students use them as-is, like a ready-made tool)

---

## What It Does
- Enter any topic (Space, Cricket, Marvel, Python, History — literally anything)
- AI generates multiple-choice questions instantly
- Take the quiz one question at a time
- Get your score with detailed explanations for every answer
