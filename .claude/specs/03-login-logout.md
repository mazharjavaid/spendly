# Spec: Login and Logout

## Overview
Implement the login and logout flows so registered users can authenticate with Spendly. This step adds a `POST /login` handler that looks up the user by email, verifies the hashed password with Werkzeug, and stores the user's `id` and `name` in the Flask session on success. A new `GET /logout` handler clears the session and redirects to the landing page. The stub `GET /login` route is upgraded to also handle `POST`. A new `get_user_by_email()` helper is added to `database/db.py` to keep SQL out of route functions. This is the first step that reads authenticated user state from the session.

## Depends on
- Step 01 — Database setup (`get_db()`, `users` table must exist)
- Step 02 — Registration (`create_user()`, `app.secret_key` already set; a user must exist to log in)

## Routes
- `POST /login` — validates email/password, sets session on success, redirects to `/profile` — public
- `GET /logout` — clears the session, redirects to `/` — public (no login required to call it)

The existing `GET /login` route is upgraded to accept `methods=["GET", "POST"]`; GET behaviour is unchanged.

## Database changes
No new tables or columns. Reads from the existing `users` table.

New helper required in `database/db.py`:
- `get_user_by_email(email)` — queries `users` by email and returns a `sqlite3.Row` (or `None` if not found). Caller is responsible for password verification.

## Templates
- **Modify:** `templates/login.html` — ensure the `<form>` has `method="POST"` and `action="{{ url_for('login') }}"`. Add a conditional error block to display `{{ error }}` when present (e.g. a styled `<p class="form-error">{{ error }}</p>` that only renders when `error` is set).
- **Modify:** `templates/base.html` — update the navbar logout link to point to `url_for('logout')` so it is no longer a dead stub.

## Files to change
- `app.py` — add `POST` to the `login` route's `methods`; add form handling and session logic; import `get_user_by_email` from `database.db`; replace the `logout` stub with a working session-clearing handler; import `session` from Flask
- `database/db.py` — add `get_user_by_email(email)` function
- `templates/login.html` — add error display block and confirm form attributes
- `templates/base.html` — wire navbar logout link to `url_for('logout')`

## Files to create
None.

## New dependencies
No new pip packages. Uses:
- `werkzeug.security.check_password_hash` — already installed
- `flask.session` — already part of Flask

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- DB logic stays in `database/db.py` — the route must not execute SQL directly
- Session keys: store `session["user_id"]` (integer) and `session["user_name"]` (string) on successful login
- On wrong email or wrong password, show the same generic error: `"Invalid email or password."` — never reveal which field was wrong
- Validate email and password are non-empty before touching the database; re-render with `error="All fields are required."` if blank
- On successful login, redirect to `url_for('profile')` — the profile stub exists and will be implemented in Step 04
- `logout` must call `session.clear()` then redirect to `url_for('landing')`
- Do not use `flask_login` or any auth extension — manage the session manually

## Definition of done
- [ ] Submitting valid email and password sets `session["user_id"]` and `session["user_name"]` and redirects to `/profile`
- [ ] Submitting an unregistered email re-renders `/login` with the generic error message and no crash
- [ ] Submitting a wrong password re-renders `/login` with the same generic error message (not a field-specific one)
- [ ] Submitting with any blank field re-renders `/login` with `"All fields are required."`
- [ ] `GET /login` still works and renders the empty form with no errors
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] The navbar logout link navigates to `/logout` (not a dead `#` href)
- [ ] `get_user_by_email()` is defined in `database/db.py`, not in `app.py`
- [ ] App starts without errors after the change
