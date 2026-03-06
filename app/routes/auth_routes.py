"""
Authentication Routes
Handles user registration, login, and logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import create_user, authenticate_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        full_name = request.form.get("full_name", "").strip()

        # ── Validation ─────────────────────────────────────────────────
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if len(password) < 4:
            flash("Password must be at least 4 characters.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        # ── Create User ────────────────────────────────────────────────
        user = create_user(username, email, password, full_name)
        if user is None:
            flash("Username already exists. Please choose another.", "error")
            return render_template("register.html")

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")

        user = authenticate_user(username, password)
        if user is None:
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        # ── Store user info in session ─────────────────────────────────
        session["user"] = user
        session["logged_in"] = True
        flash(f"Welcome back, {user.get('full_name') or user['username']}!", "success")
        return redirect(url_for("products.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Log the user out and clear session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("products.index"))
