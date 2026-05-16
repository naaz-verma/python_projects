# Web Dev Project 1: Personal Portfolio

A responsive personal portfolio website built from scratch using only HTML and CSS. No JavaScript, no Bootstrap -- pure HTML/CSS to showcase your skills and projects.

---

## Prerequisites

- Completed the Python Starter course
- Basic HTML knowledge (tags, elements, attributes)
- Basic CSS knowledge (selectors, properties, box model)

---

## What You'll Build

A professional-looking portfolio website with:
- **Fixed navigation** with smooth scrolling and a mobile hamburger menu (CSS only!)
- **Hero section** with your name, title, description, and a circular avatar
- **About section** with stats (projects built, languages learned, etc.)
- **Skills section** with animated skill bars and card layout
- **Projects section** with gradient-colored project cards
- **Contact section** with contact info cards
- **Fully responsive** -- works on phones, tablets, and desktops

---

## How to Open the Portfolio

No installation needed! Just:

1. Navigate to the `01_personal_portfolio` folder
2. Double-click `index.html` -- it opens in your browser
3. Or right-click `index.html` > "Open with" > choose your browser

To edit: open both `index.html` and `style.css` in VS Code, make changes, save, and refresh the browser.

---

## Project Files

| File | What It Does |
|------|-------------|
| `index.html` | The structure of the website (all the content and sections) |
| `style.css` | The design and layout (colors, fonts, spacing, responsive rules) |
| `README.md` | This file -- instructions and learning guide |

---

## CSS Concepts You'll Learn

### 1. CSS Variables (Custom Properties)
```css
:root {
    --primary: #6c63ff;
    --bg-dark: #1a1a2e;
}
/* Use them anywhere */
.btn { background: var(--primary); }
```
Change the color in ONE place, and it updates everywhere. Try changing `--primary` to `#e94560` and see what happens!

### 2. Flexbox (One-Dimensional Layout)
```css
.hero {
    display: flex;           /* Activate flexbox */
    align-items: center;     /* Vertical centering */
    justify-content: center; /* Horizontal centering */
    gap: 60px;               /* Space between items */
}
```
Used for: navigation, hero section, buttons, stats row.

### 3. CSS Grid (Two-Dimensional Layout)
```css
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
}
```
Used for: skills cards, project cards, contact cards. The `auto-fit` with `minmax` makes it automatically responsive!

### 4. CSS Checkbox Hack (Mobile Menu Without JavaScript)
```css
/* Hidden checkbox */
.nav-toggle { display: none; }

/* When checkbox is checked, show the menu */
.nav-toggle:checked ~ .nav-links {
    display: flex;
}
```
This is how we make the hamburger menu work without any JavaScript!

### 5. Responsive Design with Media Queries
```css
@media (max-width: 768px) {
    .hero {
        flex-direction: column-reverse; /* Stack vertically on mobile */
    }
    .skills-grid {
        grid-template-columns: 1fr;     /* One column on mobile */
    }
}
```
Two breakpoints: 768px (tablet) and 480px (small phone).

### 6. Gradients
```css
/* Text gradient */
.hero-name {
    background: linear-gradient(135deg, #6c63ff, #ff6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Background gradient */
.project-img-1 {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
```

### 7. Hover Effects & Transitions
```css
.skill-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.skill-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
```

### 8. Skill Bars (Animated Fill)
```css
.skill-bar {
    width: 100%;
    height: 8px;
    background: #1a1a2e;
    border-radius: 4px;
}
.skill-fill {
    height: 100%;
    width: 75%; /* Set in HTML via inline style */
    background: linear-gradient(90deg, #6c63ff, #ff6584);
}
```

---

## How to Customize

### Change Colors
Edit the CSS variables at the top of `style.css`:
```css
:root {
    --primary: #6c63ff;     /* Main accent color */
    --secondary: #ff6584;   /* Secondary accent */
    --bg-dark: #1a1a2e;     /* Darkest background */
}
```

### Add Your Info
In `index.html`:
1. Replace "Your Name" with your actual name
2. Update the hero description
3. Change the About section text
4. Update skill percentages (`style="width: 75%"`)
5. Add your real projects
6. Update contact info (email, GitHub, LinkedIn)

### Add a Profile Photo
Replace the avatar placeholder with an actual image:
```html
<!-- Change this: -->
<div class="avatar-placeholder">YN</div>

<!-- To this: -->
<img src="your-photo.jpg" alt="Your Name" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">
```

### Add More Projects
Copy a `project-card` div and change the content. Add a new gradient class in CSS:
```css
.project-img-5 {
    background: linear-gradient(135deg, #a18cd1, #fbc2eb);
}
```

---

## HTML Structure Summary

```
body
  |-- nav.navbar            (fixed navigation bar)
  |     |-- .logo           (site name)
  |     |-- .nav-toggle     (hidden checkbox for mobile menu)
  |     |-- .nav-links      (Home, About, Skills, Projects, Contact)
  |
  |-- section.hero          (hero with name, title, avatar)
  |-- section.about         (about text + stats)
  |-- section.skills        (6 skill cards in a grid)
  |-- section.projects      (4 project cards in a grid)
  |-- section.contact       (3 contact cards)
  |-- footer                (copyright + branding)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page looks broken | Make sure `style.css` is in the same folder as `index.html` |
| Colors not changing | Clear browser cache (Ctrl+Shift+R) after editing CSS |
| Mobile menu not working | Check the checkbox hack structure -- the input must come before the label and nav-links |
| Skill bars not showing | Check the inline `style="width: 75%"` on `.skill-fill` elements |
| Text gradient not working | The `-webkit-background-clip` property is needed for Chrome/Edge |
