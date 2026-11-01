
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "campus_lost_found_dev_key"

DATABASE = "campus.db"


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create students table
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Login protection
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


# Home page
@app.route("/")
def home():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# Student registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")

        finally:
            conn.close()

    return render_template("register.html")


# Student login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        student = conn.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if student and check_password_hash(student["password"], password):
            session.clear()
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]

            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# Student dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        name=session["student_name"]
    )


# Student logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
