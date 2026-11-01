import os
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "campus_lost_found_dev_secret_key"

DATABASE = "campus.db"
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            item_date TEXT NOT NULL,
            description TEXT,
            image_filename TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            claimer_id INTEGER NOT NULL,
            proof_description TEXT NOT NULL,
            contact_phone TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (claimer_id) REFERENCES students(id)
        )
    """)

    # Create demo student if not exists
    student = cursor.execute("SELECT id FROM students WHERE email = 'dhruv@bennett.edu.in'").fetchone()
    if not student:
        cursor.execute(
            "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
            ("Dhruv Saini", "dhruv@bennett.edu.in", generate_password_hash("password123"))
        )
        dhruv_id = cursor.lastrowid
    else:
        dhruv_id = student["id"]

    # Populate realistic campus demo items if table is empty
    item_count = cursor.execute("SELECT COUNT(*) as cnt FROM items").fetchone()["cnt"]
    if item_count == 0:
        sample_items = [
            (dhruv_id, "lost", "Casio fx-991EX Scientific Calculator", "Electronics", "LT-102 Lecture Hall", "2026-10-28", "Black calculator with name sticker 'D.S.' on the back cover.", None, "Open"),
            (dhruv_id, "found", "Bennett University Student ID Card", "ID Card / Documents", "Cafeteria Ground Floor", "2026-10-29", "ID card for CSE student found near counter 2.", None, "Open"),
            (dhruv_id, "found", "Stainless Steel Milton Water Bottle (Silver)", "Personal Belongings", "Central Library 2nd Floor", "2026-10-30", "Silver 750ml insulated bottle found near quiet cubicle.", None, "Open"),
            (dhruv_id, "lost", "Boat Rockerz 450 Bluetooth Headphones", "Electronics", "Audi-1 Corridor", "2026-10-26", "Matte black over-ear headphones in black pouch.", None, "Returned"),
            (dhruv_id, "found", "Set of 3 Keys with Ferrari Keychain", "Keys", "Sports Complex / Gym", "2026-10-31", "Two silver keys and one brass key with red lanyard.", None, "Claim Submitted"),
        ]
        cursor.executemany("""
            INSERT INTO items (student_id, type, title, category, location, item_date, description, image_filename, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_items)

        claim_item = cursor.execute("SELECT id FROM items WHERE status = 'Claim Submitted'").fetchone()
        if claim_item:
            cursor.execute("""
                INSERT INTO claims (item_id, claimer_id, proof_description, contact_phone, status)
                VALUES (?, ?, ?, ?, ?)
            """, (claim_item["id"], dhruv_id, "Hostel room 412 keys, distinct red lanyard and Ferrari badge.", "+91 9876543210", "Pending"))

    conn.commit()
    conn.close()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            flash("Please log in first to access this page.", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


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

        hashed = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed)
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        student = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        conn.close()

        if student and check_password_hash(student["password"], password):
            session.clear()
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            session["student_email"] = student["email"]
            flash(f"Welcome back, {student['name']}!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for("login"))


@app.route("/demo-auth/<target>")
def demo_auth(target):
    session["student_id"] = 1
    session["student_name"] = "Dhruv Saini"
    session["student_email"] = "dhruv@bennett.edu.in"
    return redirect(url_for(target))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    uid = session["student_id"]

    total_lost = conn.execute("SELECT COUNT(*) as c FROM items WHERE type = 'lost' AND status != 'Returned'").fetchone()["c"]
    total_found = conn.execute("SELECT COUNT(*) as c FROM items WHERE type = 'found' AND status != 'Returned'").fetchone()["c"]
    my_reports_cnt = conn.execute("SELECT COUNT(*) as c FROM items WHERE student_id = ?", (uid,)).fetchone()["c"]
    resolved_cnt = conn.execute("SELECT COUNT(*) as c FROM items WHERE status = 'Returned'").fetchone()["c"]

    my_items = conn.execute(
        "SELECT * FROM items WHERE student_id = ? ORDER BY id DESC LIMIT 5",
        (uid,)
    ).fetchall()

    recent_found = conn.execute(
        "SELECT items.*, students.name as reporter_name FROM items JOIN students ON items.student_id = students.id WHERE type = 'found' ORDER BY items.id DESC LIMIT 6"
    ).fetchall()

    # Smart match suggestions for user's open lost items
    matches = []
    my_lost_items = conn.execute(
        "SELECT * FROM items WHERE student_id = ? AND type = 'lost' AND status = 'Open'",
        (uid,)
    ).fetchall()

    for lost in my_lost_items:
        potential = conn.execute(
            """
            SELECT * FROM items 
            WHERE type = 'found' 
              AND status = 'Open' 
              AND category = ?
              AND id != ?
            LIMIT 3
            """,
            (lost["category"], lost["id"])
        ).fetchall()
        for pot in potential:
            matches.append({
                "lost_title": lost["title"],
                "lost_id": lost["id"],
                "found_item": pot
            })

    conn.close()
    return render_template(
        "dashboard.html",
        name=session["student_name"],
        total_lost=total_lost,
        total_found=total_found,
        my_reports_cnt=my_reports_cnt,
        resolved_cnt=resolved_cnt,
        my_items=my_items,
        recent_found=recent_found,
        matches=matches
    )


@app.route("/report", methods=["GET", "POST"])
@login_required
def report_item():
    if request.method == "POST":
        item_type = request.form.get("type", "lost")
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()
        item_date = request.form.get("item_date", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category or not location or not item_date:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("report_item"))

        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                fname = secure_filename(file.filename)
                fname = f"{int(os.times().elapsed*1000)}_{fname}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
                image_filename = fname

        conn = get_db()
        conn.execute(
            """
            INSERT INTO items (student_id, type, title, category, location, item_date, description, image_filename, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Open')
            """,
            (session["student_id"], item_type, title, category, location, item_date, description, image_filename)
        )
        conn.commit()
        conn.close()

        flash(f"Your {item_type.upper()} item report has been published successfully!", "success")
        return redirect(url_for("browse_items"))

    return render_template("report.html")


@app.route("/browse")
@login_required
def browse_items():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    item_type = request.args.get("type", "all").strip().lower()
    status = request.args.get("status", "all").strip()

    sql = """
        SELECT items.*, students.name as reporter_name 
        FROM items 
        JOIN students ON items.student_id = students.id 
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (items.title LIKE ? OR items.description LIKE ? OR items.location LIKE ?)"
        term = f"%{query}%"
        params.extend([term, term, term])

    if category and category != "all":
        sql += " AND items.category = ?"
        params.append(category)

    if item_type in ["lost", "found"]:
        sql += " AND items.type = ?"
        params.append(item_type)

    if status and status != "all":
        sql += " AND items.status = ?"
        params.append(status)

    sql += " ORDER BY items.id DESC"

    conn = get_db()
    items = conn.execute(sql, params).fetchall()
    conn.close()

    return render_template(
        "browse.html",
        items=items,
        query=query,
        category=category,
        item_type=item_type,
        status=status
    )


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        flash("Item not found.", "error")
        return redirect(url_for("dashboard"))

    if item["student_id"] != session["student_id"]:
        conn.close()
        flash("You can only edit items you reported.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()
        item_date = request.form.get("item_date", "").strip()
        description = request.form.get("description", "").strip()

        conn.execute(
            """
            UPDATE items 
            SET title = ?, category = ?, location = ?, item_date = ?, description = ?
            WHERE id = ?
            """,
            (title, category, location, item_date, description, item_id)
        )
        conn.commit()
        conn.close()
        flash("Item report updated successfully.", "success")
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("edit_item.html", item=item)


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if item and item["student_id"] == session["student_id"]:
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.execute("DELETE FROM claims WHERE item_id = ?", (item_id,))
        conn.commit()
        flash("Item report deleted.", "success")
    else:
        flash("Unauthorized action.", "error")

    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/items/<int:item_id>/claim", methods=["GET", "POST"])
@login_required
def claim_item(item_id):
    conn = get_db()
    item = conn.execute(
        "SELECT items.*, students.name as reporter_name FROM items JOIN students ON items.student_id = students.id WHERE items.id = ?",
        (item_id,)
    ).fetchone()

    if not item:
        conn.close()
        flash("Item not found.", "error")
        return redirect(url_for("browse_items"))

    if item["student_id"] == session["student_id"]:
        conn.close()
        flash("You cannot claim an item you reported yourself.", "error")
        return redirect(url_for("browse_items"))

    if request.method == "POST":
        proof_desc = request.form.get("proof_description", "").strip()
        phone = request.form.get("contact_phone", "").strip()

        if not proof_desc:
            flash("Please provide detailed proof of ownership.", "error")
            return redirect(url_for("claim_item", item_id=item_id))

        conn.execute(
            """
            INSERT INTO claims (item_id, claimer_id, proof_description, contact_phone, status)
            VALUES (?, ?, ?, ?, 'Pending')
            """,
            (item_id, session["student_id"], proof_desc, phone)
        )
        conn.execute("UPDATE items SET status = 'Claim Submitted' WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        flash("Your ownership claim has been submitted! The finder / admin will review your proof.", "success")
        return redirect(url_for("my_claims"))

    conn.close()
    return render_template("claim.html", item=item)


@app.route("/claims")
@login_required
def my_claims():
    uid = session["student_id"]
    conn = get_db()

    sent_claims = conn.execute(
        """
        SELECT claims.*, items.title as item_title, items.category, items.location, items.status as item_status
        FROM claims
        JOIN items ON claims.item_id = items.id
        WHERE claims.claimer_id = ?
        ORDER BY claims.id DESC
        """,
        (uid,)
    ).fetchall()

    received_claims = conn.execute(
        """
        SELECT claims.*, items.title as item_title, students.name as claimer_name, students.email as claimer_email
        FROM claims
        JOIN items ON claims.item_id = items.id
        JOIN students ON claims.claimer_id = students.id
        WHERE items.student_id = ?
        ORDER BY claims.id DESC
        """,
        (uid,)
    ).fetchall()

    conn.close()
    return render_template("claims_manage.html", sent_claims=sent_claims, received_claims=received_claims)


@app.route("/claims/<int:claim_id>/action", methods=["POST"])
@login_required
def claim_action(claim_id):
    action = request.form.get("action", "")
    conn = get_db()

    claim = conn.execute(
        "SELECT claims.*, items.student_id as item_owner_id FROM claims JOIN items ON claims.item_id = items.id WHERE claims.id = ?",
        (claim_id,)
    ).fetchone()

    if not claim:
        conn.close()
        flash("Claim record not found.", "error")
        return redirect(url_for("my_claims"))

    item_id = claim["item_id"]

    if action == "verify":
        conn.execute("UPDATE claims SET status = 'Verified' WHERE id = ?", (claim_id,))
        conn.execute("UPDATE items SET status = 'Verified' WHERE id = ?", (item_id,))
        conn.commit()
        flash("Claim verified successfully! You can coordinate handoff.", "success")
    elif action == "return":
        conn.execute("UPDATE claims SET status = 'Returned' WHERE id = ?", (claim_id,))
        conn.execute("UPDATE items SET status = 'Returned' WHERE id = ?", (item_id,))
        conn.commit()
        flash("Item has been marked as RETURNED and closed.", "success")
    elif action == "reject":
        conn.execute("UPDATE claims SET status = 'Rejected' WHERE id = ?", (claim_id,))
        conn.execute("UPDATE items SET status = 'Open' WHERE id = ?", (item_id,))
        conn.commit()
        flash("Claim rejected. Item is now open for other claimants.", "info")

    conn.close()
    return redirect(url_for("my_claims"))


if __name__ == "__main__":
    init_db()
    # Using port 5001 to avoid macOS Control Center / AirPlay conflicts on 5000
    app.run(debug=True, port=5001)
