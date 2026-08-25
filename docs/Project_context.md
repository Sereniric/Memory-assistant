# SIH 26003 — Project Context

## 1. Project Overview

**Project:** SIH 26003 MVP

**Purpose:**  
Build a simple MVP based on SIH 2026 Problem Statement 26003.

This project is being developed by a 2nd-year college team.

The team is still learning software development, so the project should prioritize:

- Simplicity
- Understandability
- Reliability
- Demonstrability
- Incremental development

We are building an MVP first rather than attempting to implement every possible feature of the problem statement.

---

# 2. Current Development Philosophy

The project should be developed incrementally.

We follow:

> Understand → Design → Implement → Test → Review → Commit

We do NOT want large amounts of code generated without understanding them.

Every major feature should be:

1. Clearly defined
2. Implemented in a simple way
3. Tested
4. Reviewed by the team
5. Committed to Git

---

# 3. Technology Stack

## Backend

- Python
- Flask

## Frontend

- HTML
- CSS
- Bootstrap CSS
- Jinja2 templates

## Database

- SQLite
- SQLAlchemy / Flask-SQLAlchemy

## Development

- Git
- GitHub
- Python virtual environment (`venv`)

## JavaScript

JavaScript is intentionally NOT being used.

The team prefers a server-side approach using Flask, Jinja2, HTML and CSS.

---

# 4. Current Architecture

The initial architecture is:

Browser
    ↓
HTML / CSS
    ↓
Flask
    ↓
Python application logic
    ↓
SQLAlchemy
    ↓
SQLite

Jinja2 is used by Flask to generate dynamic HTML pages.

---

# 5. Current Project Structure

Current structure:

sih-26003/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── __init__.py
│   ├── templates/
│   │   └── home.html
│   └── static/
│       └── css/
│           └── style.css
│
├── docs/
│   └── PROJECT_CONTEXT.md
│
├── tests/
├── instance/
│
├── venv/
├── .gitignore
├── README.md
├── requirements.txt
└── run.py

NOTE:

`venv/` is local to each developer and must NOT be committed to Git.

---

# 6. Current Application State

## Working

- Basic Flask application
- Flask application factory
- Flask Blueprint for main routes
- Jinja2 template rendering
- Basic HTML homepage
- Basic CSS styling
- Local Flask development server

## Not Implemented Yet

- User authentication
- User roles
- Database models
- SQLite database integration
- Cognitive games
- Game result tracking
- Adaptive difficulty
- Patient dashboard
- Caregiver dashboard
- Progress tracking
- Reminders
- Voice functionality
- Advanced analytics

These features must NOT be assumed to already exist.

---

# 7. MVP Direction

The MVP should focus on demonstrating the core value of the solution.

The project may eventually include:

- Elderly-friendly cognitive activities
- Memory/cognitive games
- Performance tracking
- Adaptive difficulty
- Caregiver-oriented progress information

However, features should only be added after the team agrees on them.

Do not build every possible feature at once.

---

# 8. Adaptive System

The initial adaptive system should be implemented using understandable Python rules.

We do NOT currently plan to start with machine learning.

A basic concept may be:

Performance
    ↓
Accuracy + attempts + time
    ↓
Python adaptive logic
    ↓
Next difficulty

The exact algorithm has NOT been finalized.

Do not implement an adaptive algorithm until the team defines and agrees on its behavior.

---

# 9. Database

The planned database is:

SQLite

The planned database layer is:

SQLAlchemy / Flask-SQLAlchemy

Potential entities may include:

- User
- Game
- GameResult

These are only initial concepts.

The final database schema has NOT been finalized.

Do not create unnecessary tables before the required features are defined.

---

# 10. Git Workflow

`main` is the stable branch.

Developers should NOT directly work on `main`.

Feature workflow:

main
 ↓
create feature branch
 ↓
develop
 ↓
test
 ↓
commit
 ↓
push branch
 ↓
Pull Request
 ↓
review
 ↓
merge into main

Example branch names:

feature/login
feature/memory-game
feature/caregiver-dashboard
feature/adaptive-engine

Bug fixes:

fix/login-validation
fix/game-score

---

# 11. AI Coding Agent Rules

AI coding agents may be used during development.

However, the project filesystem is the source of truth.

AI agents must:

1. Inspect the existing project before making changes.
2. Understand existing code before modifying it.
3. Avoid assuming that previous AI-generated code is correct.
4. Avoid rewriting working code unnecessarily.
5. Avoid introducing unnecessary dependencies.
6. Prefer simple solutions.
7. Explain important changes.
8. Test changes when possible.
9. Never expose or commit secrets.
10. Never modify unrelated parts of the project.

AI agents should NOT:

- Completely redesign the project without approval
- Add JavaScript
- Introduce React or Node.js
- Introduce unnecessary frameworks
- Add machine learning just to make the project appear "AI-based"
- Implement large features without first explaining the approach

---

# 12. Beginner-Friendly Development Rule

The team is composed of 2nd-year students.

Code should therefore prioritize:

- Readability
- Simple architecture
- Clear naming
- Small functions
- Understandable Python
- Minimal dependencies

Avoid unnecessary abstraction and over-engineering.

If a simple solution works, prefer the simple solution.

---

# 13. Current Milestone

## Milestone 0 — Project Foundation

Status: IN PROGRESS

Completed:

- [x] Project created
- [x] Python environment created
- [x] Flask installed
- [x] Git initialized
- [x] GitHub repository created
- [x] Basic Flask structure created
- [x] First Flask page working
- [x] Basic Git workflow established

Current task:

- [ ] Establish project documentation
- [ ] Finalize MVP requirements
- [ ] Design initial application flow

---

# 14. Important Decisions

### Decision 1 — No JavaScript

The team prefers not to use JavaScript.

The application should therefore use Flask + Jinja2 + HTML + CSS for the initial MVP.

### Decision 2 — Flask instead of FastAPI

Flask was selected because the team is beginner-level and the application will primarily use server-rendered HTML rather than being an API-first application.

### Decision 3 — SQLite

SQLite was selected because it requires minimal setup and is appropriate for an MVP.

### Decision 4 — No ML initially

The adaptive system will initially use transparent Python-based rules.

Machine learning may be considered later if there is a clear reason to introduce it.

---

# 15. Unknown / To Be Decided

The following are intentionally not finalized:

- Exact MVP feature list
- Exact game types
- User roles
- Database schema
- Adaptive difficulty algorithm
- Caregiver workflow
- Accessibility requirements
- Voice functionality
- Deployment platform
- Final UI design
- Final project architecture

Do not assume decisions for these areas.

They should be discussed and documented before implementation.

---

# 16. Change Log

## 2026-08-24

- Initial Flask project created.
- Basic homepage implemented.
- Git/GitHub workflow established.
- Initial technology stack selected.
- Initial project context created.