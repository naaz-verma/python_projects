// ===== Load config.json and populate the page =====

document.addEventListener('DOMContentLoaded', () => {
    fetch('config.json')
        .then(res => res.json())
        .then(config => buildPortfolio(config))
        .catch(err => console.error('Error loading config.json:', err));

    setupNavigation();
});

function buildPortfolio(config) {
    // Apply theme colors
    if (config.theme) {
        const root = document.documentElement;
        if (config.theme.primary_color) root.style.setProperty('--primary', config.theme.primary_color);
        if (config.theme.secondary_color) root.style.setProperty('--secondary', config.theme.secondary_color);
        if (config.theme.accent_color) root.style.setProperty('--accent', config.theme.accent_color);
    }

    // Page title
    document.title = `${config.name} | Portfolio`;

    // Navigation
    document.getElementById('nav-name').textContent = config.name.split(' ')[0];

    // Hero section
    document.getElementById('hero-name').textContent = config.name;
    document.getElementById('hero-tagline').textContent = config.tagline;
    if (config.photo) {
        document.getElementById('hero-photo').src = config.photo;
        document.getElementById('hero-photo').alt = config.name;
    }

    // About section
    document.getElementById('about-text').textContent = config.about;

    // Education
    const eduContainer = document.getElementById('education-container');
    if (config.education && config.education.length > 0) {
        config.education.forEach(edu => {
            const item = document.createElement('div');
            item.className = 'education-item';
            item.innerHTML = `
                <div class="institution">${edu.institution}</div>
                <div class="course">${edu.course}</div>
                <div class="year">${edu.year}</div>
            `;
            eduContainer.appendChild(item);
        });
    }

    // Skills
    const skillsGrid = document.getElementById('skills-grid');
    if (config.skills) {
        config.skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            skillsGrid.appendChild(tag);
        });
    }

    // Projects
    const projectsGrid = document.getElementById('projects-grid');
    if (config.projects) {
        config.projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';

            // Image or placeholder
            let imageHTML;
            if (project.image) {
                imageHTML = `<img src="${project.image}" alt="${project.title}" class="project-image"
                    onerror="this.outerHTML='<div class=\\'project-image-placeholder\\'>${project.title.charAt(0)}</div>'">`;
            } else {
                imageHTML = `<div class="project-image-placeholder">${project.title.charAt(0)}</div>`;
            }

            // Tech badges
            const techHTML = project.tech
                ? project.tech.map(t => `<span class="tech-badge">${t}</span>`).join('')
                : '';

            // Links
            let linksHTML = '';
            if (project.github_link) {
                linksHTML += `<a href="${project.github_link}" target="_blank" class="btn btn-small btn-outline">GitHub</a>`;
            }
            if (project.live_link) {
                linksHTML += `<a href="${project.live_link}" target="_blank" class="btn btn-small btn-primary">Live Demo</a>`;
            }

            card.innerHTML = `
                ${imageHTML}
                <div class="project-body">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="project-tech">${techHTML}</div>
                    <div class="project-links">${linksHTML}</div>
                </div>
            `;
            projectsGrid.appendChild(card);
        });
    }

    // Contact links
    const contactLinks = document.getElementById('contact-links');
    if (config.email) {
        contactLinks.innerHTML += `
            <a href="mailto:${config.email}" class="contact-link">
                <span class="contact-icon">&#9993;</span> Email
            </a>`;
    }
    if (config.github) {
        contactLinks.innerHTML += `
            <a href="${config.github}" target="_blank" class="contact-link">
                <span class="contact-icon">&#128187;</span> GitHub
            </a>`;
    }
    if (config.linkedin) {
        contactLinks.innerHTML += `
            <a href="${config.linkedin}" target="_blank" class="contact-link">
                <span class="contact-icon">&#128101;</span> LinkedIn
            </a>`;
    }
    if (config.resume) {
        contactLinks.innerHTML += `
            <a href="${config.resume}" target="_blank" class="contact-link">
                <span class="contact-icon">&#128196;</span> Resume
            </a>`;
    }
}

// ===== Navigation behavior =====

function setupNavigation() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    // Scroll shadow
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    });

    // Mobile toggle
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 64; // navbar height
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });
}
