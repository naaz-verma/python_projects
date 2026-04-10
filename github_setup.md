# GitHub Setup Guide - First Time

Complete steps to set up GitHub for the first time and push your project code.

---

## Step 1: Install Git

Download from [git-scm.com](https://git-scm.com/downloads) and install with default settings.

Verify it worked:
```bash
git --version
```

## Step 2: Configure Git (one-time)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Verify:
```bash
git config --global --list
```

## Step 3: Create GitHub Account

- Go to [github.com](https://github.com) and sign up
- Use the **same email** as in Step 2

## Step 4: Create a New Repository on GitHub

- Click the **+** icon (top right) > **New repository**
- Repository name: `quiz-master` (or your project name)
- Keep it **Public**
- **DO NOT** check "Add a README" or .gitignore (repo must be empty)
- Click **Create repository**

## Step 5: Navigate to the Project Folder

```bash
cd path/to/01_quiz_master
```

## Step 6: Add .gitignore (Important!)

Before pushing, make sure your API keys are not uploaded:

```bash
echo ".env" > .gitignore
```

This prevents your `.env` file (with the Gemini API key) from being pushed publicly.

## Step 7: Initialize Git and Push

```bash
git init
git add .
git commit -m "Initial commit: AI Quiz Master project"
git branch -M main
git remote add origin https://github.com/USERNAME/quiz-master.git
git push -u origin main
```

Replace `USERNAME` with your GitHub username.

## Step 8: Authenticate

On first push, a browser window will pop up asking to **Sign in to GitHub**. Log in and click **Authorize**. This saves your login so you won't need to do it again.

If the browser popup doesn't appear and it asks for a password in terminal:
- Go to GitHub > Settings > Developer Settings > **Personal Access Tokens** > **Tokens (classic)**
- Generate new token, check `repo` scope, copy the token
- Paste the token as the password when prompted

## Step 9: Verify

```bash
git status
```

Should show: `Your branch is up to date with 'origin/main'.`

Also refresh the GitHub repo page in the browser -- all files should be visible.

---

## Future Pushes

After making changes to your project:

```bash
git add .
git commit -m "Describe what changed"
git push
```
