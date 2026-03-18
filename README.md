# WorldWithWeb - Python Project Showcase

> "Don't learn to code. Code to learn."

Welcome to WorldWithWeb's Python learning track! 7 projects across different interest areas -- students pick what excites them, and learn Python through building real things.

---

## The Projects

| # | Project | What You'll Build | Interest Area | Difficulty |
|---|---------|-------------------|---------------|------------|
| 1 | [AI Quiz Master](01_quiz_master/) | AI-powered quiz app on any topic | General + AI | Beginner |
| 2 | [Space Defender](02_space_defender/) | A real playable space shooter game | Gaming | Beginner-Intermediate |
| 3 | [Password Fortress](03_password_fortress/) | Password security analyzer & cracker simulator | Cybersecurity | Intermediate |
| 4 | [AI Story Forge](04_ai_story_forge/) | Choose-your-own-adventure with AI-generated art | AI + Creative | Intermediate-Advanced |
| 5 | [Network Sentinel](05_network_sentinel/) | Network security monitoring dashboard | Cybersecurity | Advanced |
| 6 | [AI Chatbot](06_ai_chatbot/) | Chatbot with swappable personalities (Pirate, Shakespeare, etc.) | AI + Fun | Beginner |
| 7 | [AI Tutor](07_ai_tutor/) | Socratic-method AI tutor for any subject | AI + Education | Beginner-Intermediate |

---

## Quick Start

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/) (version 3.10 or higher)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (for AI projects: 1, 4, 6, 7)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get your key at: https://platform.openai.com/api-keys
```

### 4. Run a Project
```bash
# Streamlit projects (1, 3, 4, 5, 6, 7)
cd 01_quiz_master
streamlit run app.py

# Pygame project (2)
cd 02_space_defender
python main.py
```

---

## 45-Day Course Structure

Students don't do ALL projects. Based on their interest, they follow a **track** and pick 3-4 projects. Everyone learns full Python fundamentals along the way.

### Week 1-2: Python Foundations (All Students)
Everyone starts here -- core Python through hands-on exercises.
- Variables, data types, strings, numbers
- Lists, dictionaries, sets
- If/elif/else, for loops, while loops
- Functions, parameters, return values
- **Starter Project:** Project 1 (AI Quiz Master) -- everyone builds this together

### Week 3-4: Choose Your Track
Students pick their interest and build 1-2 projects from their track:

| Track | Projects | Python Concepts |
|-------|----------|-----------------|
| **AI & Creativity** | 4 (Story Forge), 6 (Chatbot), 7 (Tutor) | APIs, prompt engineering, state management |
| **Gaming** | 2 (Space Defender) | Classes, objects, game loops, OOP |
| **Cybersecurity** | 3 (Password Fortress), 5 (Network Sentinel) | Hashing, regex, sockets, threading |

### Week 5-6: Polish & Present
- Add personal touches to their project
- Prepare demo presentation
- Present to peers and parents

### After 45 Days: Keep Coming Back
Students who finish the course can:
- Build new features on their projects
- Move to the next difficulty level
- Start the "Beyond Python" track (see Career Tracks below)
- Mentor newer students

---

## Project-Interest Mapping

Not sure which projects to assign? Match the student:

| Student Interest | Recommended Projects | Why |
|-----------------|---------------------|-----|
| "I love AI / ChatGPT" | 1 + 6 + 7 | Builds real AI apps, learns prompt engineering |
| "I want to make games" | 1 + 2 | Learns OOP through game development |
| "I want to be a hacker" | 1 + 3 + 5 | Builds real security tools, understands attacks |
| "I like stories / art" | 1 + 4 | Creative AI with story generation + DALL-E art |
| "I want to build apps" | 1 + 6 + 3 | Web apps with Streamlit, API integration |
| "I'm not sure yet" | 1 + 7 + 2 | Broad exposure across AI, gaming, and learning |

---

## Career Tracks at WorldWithWeb

### Track 1: Programming & Development
```
Python Fundamentals --> These Projects --> Web Development --> Specialization
                                           (React, Node.js)   (Full-Stack, Mobile, Cloud)
```

### Track 2: Hacking & Cybersecurity
```
Python Fundamentals --> Linux --> Networking --> Cloud --> Security
                        (Kali,    (TCP/IP,      (AWS,     (Pen Testing,
                         Bash)     Wireshark)    Azure)    Bug Bounty)
```

### Track 3: Game Development
```
Python + Pygame --> Game Design --> Godot Engine --> Unity/Unreal --> Portfolio
                    (Mechanics,     (GDScript,       (C#/C++,        (Game Jams,
                     Level Design)   2D & 3D)        3D Games)       itch.io)
```

### Track 4: AI & Machine Learning
```
Python + AI APIs --> Data Science --> ML Fundamentals --> Deep Learning --> AI Products
                     (Pandas,         (scikit-learn,      (PyTorch,        (AI SaaS,
                      Plotly)          Regression)         NLP, Vision)     Agents)
```

---

## About WorldWithWeb

We help school students (8th-12th grade) discover and build their tech career -- starting with excitement, ending with expertise.

**Website:** [worldwithweb.com](https://worldwithweb.com) 