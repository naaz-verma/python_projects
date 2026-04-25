# Project 8: Smart Calculator

A Python-powered calculator web app with basic math, percentages, averages, and unit conversions — all wrapped in a clean Streamlit interface. No AI required!

---

## Prerequisites

- A laptop/PC with Windows 10 or 11
- Basic Python knowledge (variables, functions, lists, if/else)

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

1. In VS Code: **File > Open Folder** > navigate to `08_smart_calculator` folder
2. Open the terminal: **Terminal > New Terminal** (or press `` Ctrl + ` ``)
3. Make sure the terminal shows you're inside the project folder

### Step 3: Install Required Package

Run this command in the VS Code terminal:

```bash
pip install streamlit
```

If `pip` doesn't work, try:
```bash
python -m pip install streamlit
```

**What the package does:**
| Package | Why We Need It |
|---------|---------------|
| `streamlit` | Turns our Python code into a web app (no HTML/CSS needed) |

**Note:** This project does NOT need any API key. It's pure Python math — no AI, no internet required to run.

### Step 4: Run the App

From the terminal, make sure you're inside the `08_smart_calculator` folder, then run:

```bash
streamlit run app.py
```

If that doesn't work, try:
```bash
python -m streamlit run app.py
```

This will automatically open your browser at `http://localhost:8501` with the calculator running.

To **stop the app**: press `Ctrl+C` in the terminal.

---

## What It Does

- **Basic Math** — Add, subtract, multiply, divide any two numbers
- **Power & Root** — Calculate powers (x^n) and square roots
- **Percentage Calculator** — Three types: "X is what % of Y", "X% of Y", and "% change"
- **Average Calculator** — Enter comma-separated numbers, get their average
- **Unit Converter** — Convert length (mm to km), weight (g to lb), and temperature (C/F/K)
- **History** — Every calculation is saved so you can review it

---

## Project Files — What Each File Does

Read the files in this order when learning:

### File 1: `constants.py` — The Config (Read This First)

**What it does:** Stores all the fixed data the app needs — operator labels, unit conversion factors, temperature unit names.

**Key concepts for students:**
- **Constants** — Variables written in ALL_CAPS that shouldn't change
- **Dictionaries** — Mapping keys to values (e.g., unit name → conversion factor)
- **Lists** — Ordered collection (e.g., temperature unit names)

**What's inside:**
```python
OPERATORS = {"Add (+)": "+", "Subtract (-)": "-", ...}
LENGTH_UNITS = {"Meter (m)": 1.0, "Kilometer (km)": 1000.0, ...}
TEMPERATURE_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]
```

### File 2: `operations.py` — The Brain (Read This Second)

**What it does:** Contains all the math functions — add, subtract, divide, percentage, average, etc.

**Key concepts for students:**
- **Functions** — `def add(a, b): return a + b`
- **Parameters & return values** — Inputs go in, result comes out
- **Error handling with conditionals** — What if someone divides by zero?
- **Dictionary as dispatch map** — Using a dict to pick the right function
- **Using `math` module** — `math.sqrt()` for square root
- **List operations** — `sum()`, `len()` for calculating averages

**Key functions:**
```
calculate(a, b, operator)  → picks the right math operation
power(base, exponent)      → calculates x^n
square_root(number)        → calculates √x
percentage(value, total)   → what % is value of total
average(numbers)           → average of a list of numbers
```

### File 3: `converter.py` — The Converter (Read This Third)

**What it does:** Handles all unit conversions — length, weight, and temperature.

**Key concepts for students:**
- **Base-unit conversion pattern** — Convert to a common base, then to target
- **Mathematical formulas** — Temperature formulas (Celsius ↔ Fahrenheit ↔ Kelvin)
- **if/elif/else chains** — Choosing the right formula
- **Importing from other files** — `from constants import LENGTH_UNITS`

**How unit conversion works (simple explanation):**
```
User wants: 5 km → feet

Step 1: km → meters (base unit)     →  5 * 1000 = 5000 meters
Step 2: meters → feet               →  5000 / 0.3048 = 16404.2 feet
```

### File 4: `app.py` — The Face (Read This Last)

**What it does:** The web interface built with Streamlit. Connects all the pieces.

**Key concepts for students:**
- **Importing modules** — Using functions from our own files
- **Streamlit widgets** — `st.number_input()`, `st.button()`, `st.selectbox()`
- **Layout** — `st.columns()`, `st.tabs()`, `st.sidebar`
- **Session state** — `st.session_state.history` persists data between clicks
- **isinstance()** — Checking if a result is an error message (string) or a number
- **List comprehension** — `[float(n.strip()) for n in input.split(",")]`

---

## Teaching Flow (Recommended Order)

### Day 1: Python Fundamentals + Math Logic

```
Step 1: Setup           →  Install Streamlit, open project in VS Code
Step 2: constants.py    →  Explain variables, constants, dictionaries, lists
Step 3: operations.py   →  Explain functions, parameters, return values, conditionals
                           Live code: build add(), subtract(), divide() together
Step 4: Run it!         →  streamlit run app.py — see Basic Math working
Step 5: Experiment      →  Students modify operations (add modulo, add floor division)
```

### Day 2: Converters + Streamlit UI

```
Step 6: converter.py    →  Explain the base-unit conversion approach, temperature formulas
Step 7: app.py          →  Walk through Streamlit widgets, layout, session state
Step 8: Experiment      →  Students add a new conversion category (e.g., time: hours/minutes/seconds)
Step 9: Show off        →  Each student runs their modified calculator and presents changes
```

---

## How It Works (Simple Explanation)

```
User clicks "Basic Math" in sidebar
        ↓
app.py shows number inputs and operator dropdown
        ↓
User enters 10, +, 5 and clicks "Calculate"
        ↓
app.py calls calculate(10, 5, "+") from operations.py
        ↓
operations.py looks up "+" in the OPERATORS dict → calls add(10, 5)
        ↓
add() returns 15
        ↓
app.py displays "10 + 5 = 15" and saves to history
```

---

## Files

| File | What It Does |
|------|-------------|
| `app.py` | Streamlit web interface — sidebar, inputs, buttons, display |
| `operations.py` | All math functions — basic math, power, percentage, average |
| `converter.py` | Unit conversion — length, weight, temperature |
| `constants.py` | Configuration — operators, unit data, app info |

---

## Tech Stack

- Python (core logic)
- Streamlit (web interface)
- math module (square root)

---

## Quick Reference: All Terminal Commands

```bash
# ---- First time setup (run ONCE) ----

# Check Python is installed
python --version

# Install Streamlit
pip install streamlit

# ---- Every time you want to run the app ----

# Navigate to project folder (if not already there)
cd 08_smart_calculator

# Start the app
streamlit run app.py

# OR if streamlit command not found:
python -m streamlit run app.py

# Stop the app: press Ctrl+C in terminal
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install streamlit` |
| `streamlit: command not found` | Try `python -m streamlit run app.py` |
| `'python' is not recognized` | Python not installed or not in PATH. Reinstall Python and check "Add to PATH" |
| `pip: command not found` | Try `python -m pip install streamlit` instead |
| Browser doesn't open automatically | Manually go to `http://localhost:8501` in your browser |

---

## Python Concepts Used in This Project

| Concept | Where It's Used |
|---------|----------------|
| Variables & constants | `constants.py` — APP_NAME, VERSION, unit data |
| Dictionaries | Operator mapping, unit conversion factors, history entries |
| Lists | Temperature units, calculation history, number inputs |
| Functions | Every math operation is a separate function |
| Parameters & return values | `add(a, b)` takes two inputs, returns their sum |
| if/elif/else | Division by zero check, temperature conversion formulas |
| for loops | Displaying history, processing comma-separated numbers |
| Importing modules | `from operations import calculate` — using code from other files |
| f-strings | `f"{num1} {operator} {num2} = {result}"` |
| List comprehension | `[float(n.strip()) for n in input.split(",")]` |
| math module | `math.sqrt()` for square root |
| isinstance() | Checking if result is a number or an error string |
| String methods | `.strip()`, `.split(",")` for parsing user input |

**Concepts NOT needed:** Classes/OOP, APIs, API keys, AI, decorators, file I/O
