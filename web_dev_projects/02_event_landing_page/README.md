# Web Dev Project 2: Event Landing Page

A responsive event landing page for a fictional tech conference -- "TechFest 2025". Built with pure HTML and CSS, featuring a schedule with tabbed navigation, pricing cards, a registration form, and responsive design.

---

## Prerequisites

- Completed the Python Starter course
- Basic HTML knowledge (tags, elements, attributes, forms)
- Basic CSS knowledge (selectors, properties, box model, flexbox basics)

---

## What You'll Build

A complete event landing page with:
- **Hero section** with event name, date, stats, and call-to-action buttons
- **About section** with feature cards (Learn, Connect, Innovate, Compete)
- **Speakers section** with speaker cards and talk topics
- **Schedule section** with 3-day tabbed navigation (CSS only -- no JavaScript!)
- **Pricing section** with 3-tier ticket cards (Basic, Pro, VIP) with a "featured" card
- **Registration form** with text inputs, email, phone, and a dropdown
- **Venue section** with location details
- **Footer** with 3-column layout and quick links
- **Fully responsive** -- works on phones, tablets, and desktops

---

## How to Open

No installation needed! Just:

1. Navigate to the `02_event_landing_page` folder
2. Double-click `index.html` -- it opens in your browser
3. Edit files in VS Code, save, and refresh the browser

---

## Project Files

| File | What It Does |
|------|-------------|
| `index.html` | The structure and content of the landing page |
| `style.css` | All the styling, layout, and responsive rules |
| `README.md` | This file |

---

## CSS Concepts You'll Learn

### 1. CSS Variables
```css
:root {
    --primary: #e94560;
    --bg-dark: #0a0a1a;
    --text-secondary: #a0a0c0;
}
```
Change `--primary` from `#e94560` (red) to `#4ecdc4` (teal) and the entire page theme changes!

### 2. CSS-Only Tabs (Radio Button Hack)
The schedule section uses radio buttons to switch between Day 1, Day 2, and Day 3 -- no JavaScript:
```css
/* Hide the radio buttons */
.tab-input { display: none; }

/* Style the labels as tab buttons */
.tab-input:checked + .tab-label {
    background: var(--primary);
    color: white;
}

/* Show only the matching content */
#day1:checked ~ #content-day1 { display: block; }
#day2:checked ~ #content-day2 { display: block; }
#day3:checked ~ #content-day3 { display: block; }
```
The `~` (general sibling combinator) selector is the key -- it selects a sibling element that comes after the checked radio button.

### 3. CSS Grid for Card Layouts
```css
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 25px;
}
```
`auto-fit` + `minmax()` = cards automatically wrap to fewer columns on smaller screens.

### 4. Featured Pricing Card
```css
.ticket-featured {
    border-color: var(--primary);
    transform: scale(1.05);              /* Slightly larger */
    box-shadow: 0 0 30px rgba(233, 69, 96, 0.15); /* Glow effect */
}
```
The middle card "pops out" to draw attention to the most popular option.

### 5. Gradient Backgrounds
```css
.hero {
    background: linear-gradient(135deg, #0a0a1a 0%, #16213e 50%, #0f3460 100%);
}

/* Overlay with radial gradients for depth */
.hero-overlay {
    background:
        radial-gradient(circle at 20% 50%, rgba(233, 69, 96, 0.15), transparent 50%),
        radial-gradient(circle at 80% 30%, rgba(108, 99, 255, 0.1), transparent 50%);
}
```

### 6. Form Styling
```css
.form-input {
    background: rgba(255, 255, 255, 0.08);  /* Semi-transparent */
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 14px 18px;
    border-radius: 8px;
}

.form-input:focus {
    border-color: var(--primary);  /* Highlight on focus */
}

.form-input::placeholder {
    color: var(--text-secondary);  /* Style placeholder text */
}
```

### 7. Responsive Design
Two breakpoints:
```css
/* Tablet: 768px */
@media (max-width: 768px) {
    .features-grid { grid-template-columns: 1fr 1fr; }  /* 2 columns */
    .form-row { flex-direction: column; }                 /* Stack form fields */
    .footer-grid { grid-template-columns: 1fr; }          /* Single column */
}

/* Phone: 480px */
@media (max-width: 480px) {
    .features-grid { grid-template-columns: 1fr; }  /* 1 column */
    .hero-title { font-size: 2rem; }                  /* Smaller text */
}
```

### 8. CSS-Only Mobile Hamburger Menu
```css
/* Hidden checkbox controls the menu */
.nav-toggle:checked ~ .nav-links { display: flex; }

/* Animate hamburger to X */
.nav-toggle:checked ~ .nav-toggle-label span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 6px);
}
```

---

## How to Customize

### Change the Event Theme
Edit CSS variables at the top of `style.css`:
```css
:root {
    --primary: #e94560;     /* Try: #4ecdc4, #ff6348, #6c63ff */
    --bg-dark: #0a0a1a;     /* Try: #1a1a2e for lighter dark */
}
```

### Update Event Details
In `index.html`:
1. Change "TechFest 2025" to your event name
2. Update dates, venue, and descriptions
3. Change speaker names and topics
4. Update ticket prices (the &#8377; is the Rupee symbol)
5. Modify the schedule items

### Add Real Speaker Photos
Replace the placeholder:
```html
<!-- Change this: -->
<div class="speaker-placeholder">AK</div>

<!-- To this: -->
<img src="speaker-photo.jpg" alt="Speaker Name"
     style="width:100%; height:100%; border-radius:50%; object-fit:cover;">
```

---

## HTML Structure Summary

```
body
  |-- nav.navbar              (fixed navigation + mobile menu)
  |-- section.hero            (hero with title, date, stats, CTA)
  |-- section.about           (4 feature cards)
  |-- section.speakers        (4 speaker cards)
  |-- section.schedule        (3-day tabs with schedule items)
  |-- section.tickets         (3-tier pricing cards)
  |-- section.register        (registration form)
  |-- section.venue            (venue info + map placeholder)
  |-- footer                   (3-column footer + copyright)
```

---

## Comparison: Portfolio vs Landing Page

| Feature | Portfolio | Landing Page |
|---------|----------|-------------|
| Purpose | Showcase yourself | Promote an event |
| Layout | Single-page scroll | Single-page scroll |
| New CSS | Skill bars, avatar | Tabs, pricing cards, forms |
| Complexity | Simpler | More sections and interactions |
| Best for learning | Flexbox, Grid basics | CSS-only tabs, form styling, featured cards |

Both projects teach CSS Grid, Flexbox, responsive design, and CSS variables. The landing page adds form styling, CSS-only tabs (radio hack), and pricing card layouts.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page looks broken | Make sure `style.css` is in the same folder as `index.html` |
| Tabs not switching | Check that radio inputs have `name="day-tab"` and IDs match `#content-day1` etc. |
| Mobile menu not working | Verify the checkbox hack structure in the nav |
| Form not submitting | This is a static page -- the form looks complete but doesn't send data (that requires a backend) |
| Featured card not centered | On mobile, the `transform: scale(1.05)` is removed via media query |
| Rupee symbol not showing | Use `&#8377;` in HTML (that's the Unicode for &#8377;) |
