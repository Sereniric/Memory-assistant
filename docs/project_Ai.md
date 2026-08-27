# PROJECT CONTEXT — SIH 26003

## 1. PROJECT

This project is an MVP for SIH Problem 26003.

Goal: build an elderly-friendly adaptive cognitive training platform.

We are currently focusing on the first cognitive game:
**Sequence Recall**.

Keep the MVP simple, reliable, and easy to demonstrate.

---

## 2. TECH STACK

- Python
- Flask
- Jinja2
- HTML
- CSS
- Flask session for temporary game state
- SQLite + SQLAlchemy later for persistent data

### Important constraint

**DO NOT use JavaScript.**

Do not replace Flask with FastAPI.

Do not introduce unnecessary frameworks or libraries.

---

## 3. CURRENT ARCHITECTURE

```text
app/
├── __init__.py
│
├── games/
│   ├── __init__.py
│   ├── sequence_recall.py
│   └── play_sequence.py
│
├── routes/
│   ├── __init__.py
│   └── games.py
│
├── templates/
│   └── games/
│       ├── start.html
│       ├── remember.html
│       ├── answer.html
│       └── result.html
│
└── static/
    └── css/
        └── game.css

run.py
requirements.txt
.gitignore

## 9. STRICT AI DEVELOPMENT RULES

This project uses server-rendered Flask pages.

### Architecture

Use:

Python → Flask routes → Jinja2 → HTML/CSS

NOT:

JavaScript → REST API → Flask

### NEVER do these unless explicitly requested

- Do NOT create a separate standalone Flask app.
- Do NOT write `app = Flask(__name__)` inside a feature file.
- Do NOT create `/api/...` routes for normal game functionality.
- Do NOT add Flask-CORS.
- Do NOT introduce JavaScript.
- Do NOT create a separate frontend.
- Do NOT replace Jinja2 with a JavaScript framework.
- Do NOT create a second game engine.
- Do NOT duplicate existing game logic.
- Do NOT move the existing architecture.
- Do NOT rewrite `run.py` or `app/__init__.py` unnecessarily.

### IMPORTANT

The main Flask application already exists.

Features must be added to the existing application using
Blueprints, routes, templates, and existing game modules.

Before coding:

1. Read PROJECT_CONTEXT.md.
2. Inspect the existing project files.
3. Find the existing Flask application.
4. Find the existing game logic.
5. Reuse existing functions.
6. Explain which files you will modify.
7. Make the smallest required changes.
8. Test the feature.

If you think a new architecture is required, STOP and explain why.
Do not replace the existing architecture automatically.