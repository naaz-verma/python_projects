# WorldWithWeb -- Learn Tech. Build Real Things.

> "Don't learn to code. Code to learn."

We help students discover technology and build their career -- starting with excitement, ending with expertise. 20 courses across Programming, Data/AI, and Digital Skills. Every student graduates with a portfolio.

---

## The 8 Python Projects

| # | Project | What It Does | Tech |
|---|---------|--------------|------|
| 1 | [AI Quiz Master](01_quiz_master/) | AI-powered quiz app on any topic | Python, Streamlit, Gemini AI |
| 2 | [Space Defender](02_space_defender/) | Playable space shooter game | Python, Pygame |
| 3 | [Password Fortress](03_password_fortress/) | Password security analyzer & cracker simulator | Python, Streamlit |
| 4 | [AI Story Forge](04_ai_story_forge/) | Choose-your-own-adventure with AI stories | Python, Streamlit, Gemini AI |
| 5 | [Network Sentinel](05_network_sentinel/) | Network security monitoring dashboard | Python, Streamlit |
| 6 | [AI Chatbot](06_ai_chatbot/) | Chatbot with swappable personalities | Python, Streamlit, Gemini AI |
| 7 | [AI Tutor](07_ai_tutor/) | Socratic-method AI tutor for any subject | Python, Streamlit, Gemini AI |
| 8 | [Smart Calculator](08_smart_calculator/) | Calculator with unit conversion & percentages | Python, Streamlit |

---

## Repo Structure

```
python_projects/
├── 01_quiz_master/          8 Python projects (built, ready to demo)
├── 02_space_defender/
├── 03_password_fortress/
├── 04_ai_story_forge/
├── 05_network_sentinel/
├── 06_ai_chatbot/
├── 07_ai_tutor/
├── 08_smart_calculator/
├── course_structures/       20 course curriculum docs (.docx)
├── sessions/                Session guides, curriculum, bootcamps, product menu
├── trainer_handbook/         Master plan & trainer reference
├── course_projects/          Non-tech project guides & starter templates (WIP)
├── portfolio_templates/      Student portfolio website templates (WIP)
└── presentations/            Session PPT files
```

---

## Quick Start

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/) (version 3.10 or higher)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (for AI projects only: 1, 4, 6, 7)
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
# Get your key at: https://aistudio.google.com/apikey
```

### 4. Run a Project
```bash
# Streamlit projects (1, 3, 4, 5, 6, 7, 8)
streamlit run 01_quiz_master/app.py

# Pygame project (2)
python 02_space_defender/main.py
```

### 5. Run All Projects for Demo
```bash
streamlit run 01_quiz_master/app.py --server.port 8501
streamlit run 03_password_fortress/app.py --server.port 8502
streamlit run 04_ai_story_forge/app.py --server.port 8503
streamlit run 05_network_sentinel/app.py --server.port 8504
streamlit run 06_ai_chatbot/app.py --server.port 8505
streamlit run 07_ai_tutor/app.py --server.port 8506
streamlit run 08_smart_calculator/app.py --server.port 8507
python 02_space_defender/main.py
```

---

## Key Documents

| Document | What It Covers |
|----------|---------------|
| [Master Plan](trainer_handbook/worldwithweb_master_plan.md) | Complete project inventory, course-project map, teaching philosophy, implementation plan |
| [6-Week Curriculum](sessions/curriculum_6week.md) | Python school program -- phases, week-by-week, student matching |
| [Session Guides](sessions/sessions.md) | All session plans, biweekly specials, school & college segments |
| [Bootcamps](sessions/bootcamps.md) | 8 weekend skill sprint bootcamps for colleges |
| [Product Menu](sessions/product_menu.md) | External-facing course catalog with pricing |
| [Career Readiness](sessions/career_readiness.md) | Level 3 career & confidence program |

---

**WorldWithWeb** | [worldwithweb.com](https://worldwithweb.com) | +91 9872606864
