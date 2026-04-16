# Student Portfolio Template

A personal portfolio website that students customize and host for FREE using GitHub Pages.
Once set up, anyone with the link can view it — recruiters, friends, family, LinkedIn connections.

**Live URL format:** `https://yourusername.github.io`

---

## How It Works

This is a static website (HTML + CSS + JS) that reads all your information from one file: `config.json`.
You don't need to know any coding — just edit `config.json` with your details, and the website builds itself.

**You only edit ONE file: `config.json`**

The other files (`index.html`, `style.css`, `script.js`) handle the design and layout automatically. Don't touch them.

---

## End-to-End Setup Guide

### Step 1: Fork This Repository

1. Make sure you have a GitHub account (if not, go to github.com and sign up)
2. Open this repository on GitHub
3. Click the **"Fork"** button (top-right corner)
4. This creates your own copy of the portfolio under your GitHub account

### Step 2: Rename Your Repository

This is the most important step. GitHub Pages only works if the repo has a specific name.

1. In your forked repo, go to **Settings** (gear icon, top menu)
2. Under **"Repository name"**, change the name to:
   ```
   yourusername.github.io
   ```
   Replace `yourusername` with your **actual GitHub username** (case-sensitive).

   Example: If your GitHub username is `rahulsharma`, rename to `rahulsharma.github.io`
3. Click **"Rename"**

### Step 3: Enable GitHub Pages

1. Stay in **Settings**
2. Scroll down to **"Pages"** in the left sidebar (under "Code and automation")
3. Under **"Source"**, select: **Deploy from a branch**
4. Under **"Branch"**, select: **main** and folder **/ (root)**
5. Click **Save**
6. Wait 2-3 minutes

Your site is now live at: `https://yourusername.github.io`

### Step 4: Edit config.json With Your Details

1. Go back to your repo's main page (click the repo name at the top)
2. Click on `config.json` to open it
3. Click the **pencil icon** (top-right of the file) to edit
4. Replace all placeholder values with your real information:

```json
{
  "name": "Rahul Sharma",
  "tagline": "Python Developer | WorldWithWeb Graduate",
  "about": "I am a Python developer who loves building web apps. I completed my training at WorldWithWeb where I built 3 projects using Python and Streamlit.",
  "photo": "assets/photo.jpg",
  "email": "rahul.sharma@gmail.com",
  "github": "https://github.com/rahulsharma",
  "linkedin": "https://linkedin.com/in/rahulsharma",
  "resume": "assets/resume.pdf",
  "skills": [
    "Python",
    "Streamlit",
    "HTML & CSS",
    "Git & GitHub",
    "AI Prompting"
  ],
  "projects": [
    {
      "title": "AI Quiz Master",
      "description": "An AI-powered quiz app that generates questions on any topic using Google Gemini. Built with Streamlit.",
      "tech": ["Python", "Streamlit", "Gemini AI"],
      "image": "assets/project1.png",
      "github_link": "https://github.com/rahulsharma/quiz-master",
      "live_link": ""
    }
  ],
  "education": [
    {
      "institution": "WorldWithWeb",
      "course": "Python Complete (3 Months)",
      "year": "2026"
    }
  ],
  "theme": {
    "primary_color": "#4472C4",
    "secondary_color": "#2c3e50",
    "accent_color": "#e74c3c",
    "font": "Inter"
  }
}
```

5. After editing, scroll down and click **"Commit changes"**
6. Wait 1-2 minutes, then refresh your live site to see the updates

### Step 5: Upload Your Photo and Project Screenshots

1. In your repo, click on the `assets` folder
2. Click **"Add file"** > **"Upload files"**
3. Upload these files:
   - `photo.jpg` — Your profile photo (square, 300x300px recommended)
   - `project1.png` — Screenshot of your first project
   - `project2.png` — Screenshot of your second project
   - `resume.pdf` — Your resume (optional)
4. Click **"Commit changes"**

**How to take project screenshots:**
- Run your project, and press `Win + Shift + S` (Windows) or `Cmd + Shift + 4` (Mac)
- Crop to show the best part of your project
- Save as PNG

### Step 6: Share Your Portfolio

Your portfolio is now live and public. Anyone with the link can view it.

**Your URL:** `https://yourusername.github.io`

Share it on:
- **LinkedIn** — Add it to your profile under "Website" or in your headline
- **Resume** — Add the URL under your contact details
- **WhatsApp/Email** — Send the link directly to anyone
- **Job Applications** — Paste the URL in "Portfolio" or "Website" fields

---

## What to Edit (Summary)

| File | What to change | How |
|------|---------------|-----|
| `config.json` | Your name, tagline, about, skills, projects, links, colors | Click file > pencil icon > edit > commit |
| `assets/photo.jpg` | Your profile photo | Upload via Add file > Upload files |
| `assets/project1.png` | Project screenshot | Upload via Add file > Upload files |
| `assets/resume.pdf` | Your resume (optional) | Upload via Add file > Upload files |

**Files you should NOT edit:**

| File | What it does |
|------|-------------|
| `index.html` | Page structure (auto-loads your config.json) |
| `style.css` | Visual design and responsive layout |
| `script.js` | Reads config.json and builds the page |

---

## Adding More Projects Later

You can keep adding projects even after the course ends. Edit `config.json` and add a new entry to the `projects` array:

```json
{
    "title": "My New Project",
    "description": "What this project does and what I learned.",
    "tech": ["Python", "Streamlit"],
    "image": "assets/project4.png",
    "github_link": "https://github.com/yourusername/project",
    "live_link": ""
}
```

Don't forget to upload `project4.png` to the `assets` folder.

---

## Customizing Colors

Change the `theme` section in `config.json` to personalize your site:

```json
"theme": {
    "primary_color": "#4472C4",
    "secondary_color": "#2c3e50",
    "accent_color": "#e74c3c",
    "font": "Inter"
}
```

Some color ideas:
- Blue theme: `"#4472C4"` (default)
- Green theme: `"#27ae60"`
- Purple theme: `"#8e44ad"`
- Teal theme: `"#16a085"`
- Orange theme: `"#e67e22"`

Use any hex color code — search "color picker" on Google to find one you like.

---

## Testing Locally (For Trainers)

If you want to preview the site on your computer before pushing to GitHub:

1. Open a terminal/command prompt
2. Navigate to this folder:
   ```
   cd portfolio_templates/github_pages
   ```
3. Start a local server:
   ```
   python -m http.server 8080
   ```
4. Open browser and go to: `http://localhost:8080`
5. Press `Ctrl+C` in terminal to stop the server when done

**Note:** Double-clicking `index.html` directly will NOT work. The site uses JavaScript `fetch()` to load `config.json`, which requires a web server. The local server command above handles this. On GitHub Pages, this works automatically.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Site shows 404 error | Repo name must be exactly `yourusername.github.io` (case-sensitive). Check Settings > Pages is enabled. |
| Changes not showing on live site | GitHub Pages takes 1-3 minutes to update after a commit. Hard refresh: `Ctrl+Shift+R` |
| Photo not loading | File name must match exactly what is in config.json (case-sensitive). Must be in `assets/` folder. |
| Page shows "Loading..." | config.json has a syntax error. Check for missing commas, extra commas, or unclosed quotes. Use jsonlint.com to validate. |
| Project images show a letter instead of image | The image file doesn't exist in `assets/`. Upload it, or remove the `"image"` line from config.json. The letter fallback is intentional. |
| Site looks broken on phone | It shouldn't — the design is responsive. Clear your browser cache and refresh. |

---

## FAQ

**Q: Is this really free?**
Yes. GitHub Pages is free for public repositories. No credit card needed.

**Q: Can I use a custom domain (like myname.com)?**
Yes, but you need to buy a domain (~Rs 500-800/year). GitHub Pages supports custom domains. Ask your trainer for help.

**Q: Will the site stay live forever?**
As long as your GitHub account exists and the repo is public, yes.

**Q: Can I update it after the course?**
Yes. Just edit config.json on GitHub anytime. Changes go live in 1-2 minutes.

**Q: What if I don't have LinkedIn?**
Leave the `linkedin` field as `""` (empty string). The LinkedIn button won't show.

**Q: Do I need to know HTML/CSS/JS?**
No. You only edit config.json. The website handles everything else automatically.

---

Built with WorldWithWeb. Learn. Build. Amplify.
