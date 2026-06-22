# Spec: Registration

## Overview
Implement the user registration flow so new visitors can create a Spendly account. This step adds a `POST /register` handler that validates input, hashes the password, and inserts a new row into the `users` table via a `create_user()` helper in `database/db.py`. It also sets `app.secret_key` to enable Flask sessions (required by later steps). On success the user is shown with a sucess mmessage and redirected to `/login`; on failure (duplicate email or blank fields) the form re-renders with an inline error message. This is the first step that writes user-generated data to the database.

## Depends on
- Step 01 — Database setup (`get_db()`, `init_db()`, `users` table must exist and be initialised on startup)

## Routes
- `POST /register` — validates fields, creates user, redirects to `/login` on success — public

The existing `GET /register` route is unchanged; it continues to render `register.html`.

## Database changes
No new tables or columns. Uses the existing `users` table.

New helper required in `database/db.py`:
- `create_user(name, email, password)` — hashes the password with `generate_password_hash`, inserts the row, commits, and returns the new user `id`. Raises `sqlite3.IntegrityError` on duplicate email (caller handles it).

## Templates
- **Modify:** `templates/register.html` — ensure the `<form>` has `method="POST"` and `action="{{ url_for('register') }}"`. Add a conditional error block to display `{{ error }}` when present (e.g. a styled `<p class="form-error">{{ error }}</p>` that only renders when `error` is set).

## Files to change
- `app.py` — set `app.secret_key`; add `POST` to the `register` route's `methods`; add form handling logic; import `create_user` from `database.db`
- `database/db.py` — add `create_user(name, email, password)` function
- `templates/register.html` — add error display block and confirm form attributes

## Files to create
None.

## New dependencies
No new pip packages. Uses:
- `werkzeug.security.generate_password_hash` — already installed
- `flask.request`, `flask.redirect`, `flask.url_for` — already part of Flask

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never store plaintext
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- DB logic stays in `database/db.py` — the route must not execute SQL directly
- `app.secret_key` must be set on the `app` object before any route is registered; use a hardcoded dev string (`"dev-secret-change-in-prod"`) for now
- On duplicate email, catch `sqlite3.IntegrityError` in the route and re-render the form with `error="An account with that email already exists."`
- Validate `name`, `email`, and `password` are all non-empty before touching the database; re-render with an appropriate `error` message if any field is blank
- On success, redirect to `url_for('login')` — do not auto-login the user in this step

## Definition of done
- [ ] Submitting the form with valid name, email, and password inserts a new row in `users` with a hashed (not plaintext) password and redirects to `/login`
- [ ] Submitting with an already-registered email re-renders `/register` with a visible error message and no crash
- [ ] Submitting with any blank field re-renders `/register` with a visible error message
- [ ] `GET /register` still works and renders the empty form with no errors
- [ ] The `password_hash` column in the database never contains the raw password string
- [ ] App starts without errors after the change
- [ ] `create_user()` is defined in `database/db.py`, not in `app.py`
