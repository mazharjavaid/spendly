# CLAUDE.md

## Project overview

Spendly is a lightweight personal expense tracker built with Flask and SQLite.

---

## Architecture
```
spendly/
├── app.py              # All routes — single file, no blueprints
├── database/
│   └── db.py           # SQLite helpers: get_db(), init_db(), seed_db()
├── templates/
│   ├── base.html       # Shared layout — all templates must extend this
│   └── *.html          # One template per page
├── static/
│   ├── css/
│   │   ├── style.css       # Global styles
│   │   └── landing.css     # Landing-page-only styles
│   └── js/
│       └── main.js         # Vanilla JS only
└── requirements.txt
```

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Page-specific styles → new `.css` file, not inline `<style>` tags

---

## Code style

- Python: PEP 8, snake_case for all variables and functions
- Templates: Jinja2 with `url_for()` for every internal link — never hardcode URLs
- Route functions: one responsibility only — fetch data, render template, done
- DB queries: always use parameterized queries (`?` placeholders) — never f-strings in SQL
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

---

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** — work within `requirements.txt` as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and `match` statements are fine

---

## Subagent Policy
- Always use a builtin explore subagent for codebase exploration 
  before implementing any new feature
- Always use a subagent to verify test results 
  after any implementation
- When asked to plan, delegate codebase research 
  to a subagent before presenting the plan
- always use a builtin plan subagent in plan mode

---

## Commands
```bash
# Setup
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server (port 5001)
python app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

Start the app from the project folder:

cd "e:\O.S\Projects\ClaudeCode\expense-tracker"
py -3 app.py
Open http://127.0.0.1:5001 in your browser while the server is running.

---

## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` |
| `GET /login` | Implemented — renders `login.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

**Do not implement a stub route unless the active task explicitly targets that step.**

---

## Warnings and things to avoid

- **Never use raw string returns for stub routes** once a step is implemented — always render a template
- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** mid-feature without flagging it — keep `requirements.txt` in sync
- **Never use JS frameworks** — the frontend is intentionally vanilla
- **`database/db.py` is currently empty** — do not assume helpers exist until the step that implements them
- **FK enforcement is manual** — SQLite foreign keys are off by default; `get_db()` must run `PRAGMA foreign_keys = ON` on every connection
- The app runs on **port 5001**, not the Flask default 5000 — don't change this



---
---




### Stack

- **Backend:** Flask 3.1.3, Werkzeug — Python, no ORM
- **Database:** SQLite (file: `expense_tracker.db`, git-ignored); connection logic goes in `database/db.py`
- **Templating:** Jinja2 server-side rendering; `render_template()` returns full HTML pages
- **Frontend:** Vanilla CSS + JS; no build step, no bundler

### Key files

- `app.py` — All routes defined here via `@app.route` decorators. Contains implemented routes (`/`, `/login`, `/register`, `/terms`, `/privacy`) and stub routes with step-number comments (`/logout`, `/profile`, `/expenses/...`)
- `database/db.py` — Placeholder; students implement `get_db()`, `init_db()`, `seed_db()`
- `templates/base.html` — Parent template with sticky navbar (brand: "Spendly"), footer, and `{% block content %}` slot
- `static/css/style.css` — Single unified stylesheet; all CSS lives here
- `static/js/main.js` — Placeholder for JS

### CSS design system

CSS custom properties defined at `:root` in `style.css`:
- Colors: `--ink` (dark), `--paper` (light), `--accent-green`, `--accent-amber`, `--danger`
- Fonts: `--font-display` (DM Serif Display), `--font-body` (DM Sans) — loaded from Google Fonts in `base.html`
- Layout: `--max-width: 1200px`, `--auth-width: 440px`
- Responsive breakpoints: 900px and 600px

### Routing pattern

All routes render Jinja2 templates. Templates use `url_for('view_function_name')` for URL generation. Stub routes are marked with `# Step N:` comments indicating the next implementation phase.

### Database (not yet implemented)

The planned schema uses SQLite with foreign keys enabled. The `database/db.py` module will expose `get_db()` (returns a connection with `row_factory = sqlite3.Row`), `init_db()` (creates tables), and `seed_db()` (inserts sample data). The app does not use Flask-SQLAlchemy — raw `sqlite3` module only.
