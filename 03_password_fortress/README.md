# Project 3: Password Fortress

A cybersecurity tool that analyzes password strength, simulates how attackers crack passwords, and teaches you to build unbreakable passwords -- all from your browser.

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, dictionaries, loops, if/else, strings)

---

## What Is This Project About?

Every website you use stores your password. If that password is weak, attackers can crack it in seconds. This project teaches you **how passwords get attacked** and **how to defend yourself** -- by building a tool that does both.

You'll build a web app with 4 features:
1. **Analyze** any password and see how strong it really is
2. **Simulate** how hackers crack passwords (brute force & dictionary attacks)
3. **Generate** strong random passwords and passphrases
4. **Learn** the science behind password security (entropy, hashing, attack methods)

> **Important:** This is a 100% safe, educational tool. The crack simulator only works on passwords you type into the app -- it doesn't access anything else on your computer or the internet.

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

Also verify pip:

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

1. In VS Code: **File > Open Folder** > navigate to `03_password_fortress` folder
2. Open the terminal: **Terminal > New Terminal** (or press `` Ctrl + ` ``)
3. Make sure the terminal shows you're inside the project folder

### Step 3: Install Required Packages

Run these commands **one by one** in the VS Code terminal:

```bash
pip install streamlit
pip install plotly
```

If `pip` doesn't work, try with `python -m pip` instead:
```bash
python -m pip install streamlit
python -m pip install plotly
```

**What each package does:**
| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Turns our Python code into a web app (no HTML/CSS needed) |
| `plotly` | Creates interactive charts (the strength gauge, bar charts) |

**Note:** This project also uses `hashlib`, `re`, `math`, `string`, `itertools`, `random`, `time`, and `os` -- but these all come **built-in with Python**. No installation needed for them.

### Step 4: Run the App

From the terminal, make sure you're inside the `03_password_fortress` folder, then run:

```bash
streamlit run app.py
```

If that doesn't work, try:
```bash
python -m streamlit run app.py
```

This will automatically open your browser at `http://localhost:8501` with the app running.

To **stop the app**: press `Ctrl+C` in the terminal.

---

## Project Files -- What Each File Does

Read the files in this order when learning:

### File 1: `analyzer.py` -- The Detective (Read This First)

**What it does:** Takes any password and tells you exactly how strong or weak it is.

**Key concepts for students:**
- `re.search()` -- uses **regular expressions** to check if a password contains uppercase, lowercase, digits, or special characters
- `math.log2()` -- calculates **entropy** (the mathematical randomness of your password)
- `pool_size` -- the total number of possible characters (e.g., if you use lowercase + digits, pool = 26 + 10 = 36)
- Pattern detection -- checks for common weak patterns like "123", "qwerty", repeated characters, leet speak (@ for a, 0 for o)

**Five functions, all readable:**
```
analyze_password()     --> Main function: analyzes everything, returns a dictionary of results
detect_patterns()      --> Checks for weak patterns (sequential, keyboard, common words)
calculate_score()      --> Gives a 0-100 score based on length, variety, entropy, patterns
estimate_crack_time()  --> How long it would take to crack at different speeds
format_time()          --> Converts seconds into "3 days" or "2 million years"
is_common_password()   --> Checks against the 1000+ leaked passwords file
```

**Important Python you'll learn here:**
```python
# Regular expressions (re module)
has_upper = bool(re.search(r"[A-Z]", password))    # Does it have uppercase?
has_digit = bool(re.search(r"\d", password))         # Does it have numbers?

# Entropy formula
entropy = length * math.log2(pool_size)              # Randomness in bits

# Checking patterns with "in"
if "qwerty" in password.lower():                     # Is "qwerty" inside the password?

# Reading a file into a set
with open("common_passwords.txt", "r") as f:
    common = {line.strip().lower() for line in f}    # Set comprehension!
```

### File 2: `cracker_sim.py` -- The Attacker (Read This Second)

**What it does:** Simulates two real attack methods that hackers use -- safely and educationally.

**Key concepts for students:**
- `hashlib.sha256()` -- converts a password into a **hash** (a scrambled string). Websites store hashes, not your actual password
- `itertools.product()` -- generates every possible combination of characters (the core of brute force)
- `time.time()` -- measures how long the attack takes
- Dictionary attacks -- trying common words + their variations (password1, Password!, p@ssword)

**Three functions:**
```
hash_password()          --> Converts text to SHA-256 or MD5 hash
brute_force_sim()        --> Tries every combination (a, b, c... aa, ab, ac...) until it finds a match
dictionary_attack_sim()  --> Tries common passwords and their variations
generate_variations()    --> Creates variations of a word (capitalize, add "123", leet speak)
```

**Important Python you'll learn here:**
```python
# Hashing (one-way encryption)
hashlib.sha256("hello".encode()).hexdigest()
# Returns: "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

# Generating all combinations with itertools
for guess in itertools.product("abc", repeat=2):
    # ("a","a"), ("a","b"), ("a","c"), ("b","a"), ("b","b")... etc.
    password = "".join(guess)   # "aa", "ab", "ac", "ba", "bb"...

# Timing code
start = time.time()
# ... do work ...
elapsed = time.time() - start    # How many seconds it took
```

### File 3: `generator.py` -- The Builder (Read This Third)

**What it does:** Creates strong random passwords and memorable passphrases.

**Key concepts for students:**
- `random.choice()` -- picks a random character from a string
- `random.sample()` -- picks multiple random items without repeats
- `random.shuffle()` -- shuffles a list in place (so required characters aren't always first)
- `string.ascii_lowercase` / `string.digits` -- built-in character sets

**Two functions:**
```
generate_password()    --> Creates a random password with configurable options
generate_passphrase()  --> Picks random words and joins them ("Tiger-Storm-Noble-Quest")
```

**Important Python you'll learn here:**
```python
# String module gives you ready-made character sets
string.ascii_lowercase    # "abcdefghijklmnopqrstuvwxyz"
string.ascii_uppercase    # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
string.digits             # "0123456789"

# Random selections
random.choice("abcdef")           # Pick one random character
random.sample(word_list, 4)       # Pick 4 random words (no repeats)

# String replace for excluding characters
lower = "abcdefghijklmnopqrstuvwxyz"
lower = lower.replace("l", "").replace("o", "")   # Remove ambiguous chars
```

### File 4: `app.py` -- The Face (Read This Last)

**What it does:** The web interface using Streamlit -- connects all the other files together.

**Key concepts for students:**
- `st.tabs()` -- creates tab navigation (Analyze, Crack, Generate, Learn)
- `st.text_input()` with `type="password"` -- creates a password field (dots instead of text)
- `st.button()` -- creates clickable buttons
- `st.columns()` -- splits the page into side-by-side columns
- `st.progress()` -- shows a progress bar (used during brute force)
- `go.Figure(go.Indicator(...))` -- creates the circular strength gauge using Plotly

### File 5: `common_passwords.txt` -- The Database

A list of 1000+ most commonly leaked passwords from real data breaches. The analyzer checks your password against this list.

---

## Cybersecurity Concepts You'll Understand After This Project

### What is Hashing?
When you create a password on a website, they don't store "MyPassword123". They store a **hash** -- a scrambled version:
```
"MyPassword123" --> SHA-256 --> "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"
```
- Hashing is **one-way** -- you can't reverse the hash back to the password
- Same input always gives same output
- Attackers try to crack hashes by guessing passwords and comparing hashes

### What is Entropy?
Entropy = how random/unpredictable your password is, measured in **bits**.
- Formula: `entropy = length x log2(pool_size)`
- A 12-char password using all character types (94 chars): `12 x log2(94) = 78.7 bits`
- Below 28 bits = cracked instantly. Above 60 bits = practically safe.

### How Do Attackers Crack Passwords?

| Attack Method | How It Works | Example |
|---------------|-------------|---------|
| **Brute Force** | Try every possible combination: a, b, c... aa, ab, ac... | Slow but guaranteed to find it eventually |
| **Dictionary Attack** | Try common words + variations: password, Password1, p@ssword | Fast -- catches 80%+ of weak passwords |
| **Rainbow Table** | Pre-computed hash lookup table | Nearly instant for common passwords |
| **Credential Stuffing** | Use leaked passwords from other sites | If you reuse passwords, you're vulnerable |

### Rules for Strong Passwords
1. **Length > Complexity** -- a 20-character passphrase beats a short complex password
2. **Never reuse** passwords across sites
3. **Use a password manager** (Bitwarden, 1Password, KeePass)
4. **Enable 2FA** (Two-Factor Authentication) wherever possible
5. **Avoid personal info** -- no birthdays, pet names, or phone numbers

---

## Teaching Flow (Recommended Order)

```
Step 1: Context        --> "What happens when your password gets leaked?"
Step 2: Setup          --> Install packages, run the app
Step 3: analyzer.py    --> How do we measure password strength? Regex, entropy, patterns
Step 4: cracker_sim.py --> How do hackers actually crack passwords? Hashing, brute force, dictionaries
Step 5: generator.py   --> How do we create strong passwords? Randomness, string module
Step 6: app.py         --> How does Streamlit connect it all? Tabs, buttons, charts
Step 7: Experiment     --> Try cracking your own passwords, generate new ones, compare entropy
```

---

## How It Works (Simple Explanation)

```
User types a password in the Analyze tab
        |
analyzer.py checks:
   - Length, uppercase, lowercase, digits, special chars
   - Calculates entropy (randomness in bits)
   - Detects weak patterns (123, qwerty, common words)
   - Estimates crack time at different speeds
   - Checks against 1000+ leaked passwords
        |
app.py displays:
   - A color-coded strength gauge (0-100)
   - Character analysis breakdown
   - Crack time estimates
   - Pattern warnings

---

User clicks "Run Brute Force" in the Crack tab
        |
cracker_sim.py:
   - Hashes the target password with SHA-256
   - Generates every combination: a, b, c... aa, ab...
   - Hashes each guess and compares to target hash
   - Shows attempt count, time, speed in real-time
        |
app.py shows: "Cracked in 23,456 attempts, 1.2 seconds"

---

User clicks "Generate Password" in the Generate tab
        |
generator.py:
   - Builds a character set based on user options
   - Picks random characters using random.choice()
   - Ensures at least one character from each type
   - Shuffles the result
        |
app.py shows: the password + its strength score + entropy
```

---

## Quick Reference: All Terminal Commands

```bash
# ---- First time setup (run ONCE) ----

# Check Python is installed
python --version

# Check pip is installed
pip --version

# Install required packages
pip install streamlit
pip install plotly

# ---- Every time you want to run the app ----

# Navigate to project folder (if not already there)
cd 03_password_fortress

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
pip show plotly
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install streamlit` |
| `ModuleNotFoundError: No module named 'plotly'` | Run `pip install plotly` |
| `streamlit: command not found` | Try `python -m streamlit run app.py` |
| `'python' is not recognized` | Python not installed or not in PATH. Reinstall Python and check "Add to PATH" |
| `pip: command not found` | Try `python -m pip install ...` instead of `pip install ...` |
| Brute force is very slow | This is expected -- it's trying every combination. Keep passwords short (4-5 chars) for the demo |
| Gauge chart not showing | Make sure Plotly is installed: `pip show plotly` |
| Browser doesn't open automatically | Manually go to `http://localhost:8501` in your browser |
| `FileNotFoundError: common_passwords.txt` | Make sure you're running from inside the `03_password_fortress` folder |

---

## Python Concepts Used in This Project

| Concept | Where It's Used |
|---------|----------------|
| Variables & strings | Password input, character sets, hash values |
| Lists | Storing patterns, variations, word lists |
| Dictionaries | Returning analysis results (`{"score": 85, "entropy": 78.7, ...}`) |
| Sets | `{line.strip() for line in f}` -- set comprehension for fast password lookup |
| Functions | `analyze_password()`, `hash_password()`, `generate_password()`, etc. |
| f-strings | `f"Strength: {result['strength']}"` |
| for loops | Iterating through combinations, patterns, wordlists |
| if/elif/else | Score ranges, strength labels, pattern checks |
| `import` | Using `re`, `math`, `hashlib`, `itertools`, `random`, `string`, `time` modules |
| Regular expressions | `re.search(r"[A-Z]", password)` -- pattern matching in strings |
| File I/O | Reading `common_passwords.txt` with `open()` and `with` statement |
| Math operations | Entropy calculation with `math.log2()`, exponentiation for combinations |
| `itertools.product()` | Generating all possible character combinations for brute force |
| `time.time()` | Measuring how long operations take |
| `random.choice()` / `random.sample()` / `random.shuffle()` | Password and passphrase generation |

**Concepts NOT needed:** Classes/OOP, APIs, networking -- this project is pure Python logic.

---

## What It Does
- Enter any password and see its true strength (score, entropy, patterns, crack time)
- Watch a brute force attack try every combination in real-time
- See how dictionary attacks crack common passwords in seconds
- Generate strong random passwords and memorable passphrases
- Learn the cybersecurity fundamentals behind password security
