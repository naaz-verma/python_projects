# Project 3: Password Fortress

A cybersecurity tool that analyzes password strength, simulates how attackers crack passwords, and teaches you to build unbreakable passwords.

## What It Does
- Analyzes any password for strength (length, complexity, patterns)
- Shows estimated crack time for different attack methods
- Simulates brute force and dictionary attacks (educational)
- Generates strong random passwords
- Checks against a list of commonly leaked passwords
- Visualizes password entropy

## How to Run
```bash
cd 03_password_fortress
streamlit run app.py
```

## Python Concepts You'll Learn
- String methods (upper, lower, isdigit, etc.)
- Sets and character analysis
- Math operations (entropy, combinations)
- Hashing (SHA-256, MD5)
- Regular expressions (pattern detection)
- File I/O (reading wordlists)
- Algorithms (brute force simulation)
- Data visualization with Plotly

## Files
| File | What It Does |
|------|-------------|
| `app.py` | Streamlit web interface for all features |
| `analyzer.py` | Password strength analysis engine |
| `cracker_sim.py` | Brute force & dictionary attack simulator |
| `generator.py` | Secure password generator |
| `common_passwords.txt` | Top 1000 most common passwords |

## Tech Stack
- Python
- Streamlit (web interface)
- Plotly (charts)
- hashlib (hashing)
