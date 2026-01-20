from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey"


# ---------- DATABASE ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            age INTEGER,
            bp INTEGER,
            sugar INTEGER,
            smoking TEXT,
            family_history TEXT,
            risk TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT age, bp, sugar, smoking, family_history, risk
        FROM health_records
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )
    records = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", records=records)


@app.route("/health", methods=["GET", "POST"])
def health():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        age = int(request.form["age"])
        bp = int(request.form["bp"])
        sugar = int(request.form["sugar"])
        smoking = request.form["smoking"]
        family_history = request.form["family_history"]

        risk = "Low"
        if sugar > 200 or bp > 140 or smoking == "yes":
            risk = "High"
        elif sugar > 140 or bp > 120:
            risk = "Medium"

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO health_records
            (user_id, age, bp, sugar, smoking, family_history, risk)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                age,
                bp,
                sugar,
                smoking,
                family_history,
                risk
            )
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("health.html")


@app.route("/awareness")
def awareness():
    return render_template("awareness.html")


@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM health_records")
    total_checks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health_records WHERE risk = 'High'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health_records WHERE risk = 'Medium'")
    medium_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health_records WHERE risk = 'Low'")
    low_risk = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        total_checks=total_checks,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk
    )


# ---------- START ----------
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
