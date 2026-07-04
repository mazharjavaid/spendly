import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="An account with that email already exists.",
            )

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            return render_template("login.html", error="All fields are required.")

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session.clear()
        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "initials": "DU",
        "member_since": "March 2026",
    }

    stats = [
        {"label": "Total Spent",  "value": "Rs. 14,000", "sub": "This year", "sub_class": ""},
        {"label": "Transactions", "value": "8",          "sub": "Recorded",  "sub_class": ""},
        {"label": "Top Category", "value": "Shopping",   "sub": "Rs. 4,500 spent", "sub_class": "profile-sub-accent"},
    ]

    transactions = [
        {"date": "2026-06-20", "description": "Dinner with friends",     "category": "Food",          "amount": "Rs. 1,100"},
        {"date": "2026-06-17", "description": "Stationery",              "category": "Other",         "amount": "Rs. 600"},
        {"date": "2026-06-14", "description": "Shoes from Dolmen",       "category": "Shopping",      "amount": "Rs. 4,500"},
        {"date": "2026-06-11", "description": "Cinema tickets",          "category": "Entertainment", "amount": "Rs. 2,000"},
        {"date": "2026-06-09", "description": "Pharmacy",                "category": "Health",        "amount": "Rs. 1,200"},
        {"date": "2026-06-06", "description": "Electricity bill",        "category": "Bills",         "amount": "Rs. 3,500"},
        {"date": "2026-06-04", "description": "Uber to office",          "category": "Transport",     "amount": "Rs. 250"},
        {"date": "2026-06-02", "description": "Biryani from Burns Road", "category": "Food",          "amount": "Rs. 850"},
    ]

    categories = [
        {"name": "Shopping",      "amount": "Rs. 4,500", "width_class": "profile-bar-w30"},
        {"name": "Bills",         "amount": "Rs. 3,500", "width_class": "profile-bar-w25"},
        {"name": "Entertainment", "amount": "Rs. 2,000", "width_class": "profile-bar-w15"},
        {"name": "Food",          "amount": "Rs. 1,950", "width_class": "profile-bar-w15"},
        {"name": "Health",        "amount": "Rs. 1,200", "width_class": "profile-bar-w10"},
        {"name": "Other",         "amount": "Rs. 600",   "width_class": "profile-bar-w05"},
        {"name": "Transport",     "amount": "Rs. 250",   "width_class": "profile-bar-w05"},
    ]

    return render_template(
        "profile.html",
        user=user, stats=stats, transactions=transactions, categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
