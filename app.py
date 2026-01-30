from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ===============================
# DATABASE CONNECTION
# ===============================
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ===============================
# DATABASE SETUP
# ===============================
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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
            risk TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


# ===============================
# RISK CALCULATION LOGIC
# ===============================
def calculate_risk(age, bp, sugar, smoking, family_history):
    score = 0

    if bp > 140:
        score += 1
    if sugar > 180:
        score += 1
    if smoking == "yes":
        score += 1
    if family_history == "yes":
        score += 1

    if score >= 3:
        return "High"
    elif score == 2:
        return "Medium"
    else:
        return "Low"


# ===============================
# ROUTES
# ===============================

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not name or not email or not password:
            error = "All fields are required."
        else:
            try:
                conn = get_db_connection()
                conn.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password)
                )
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                error = "Email already registered."

    return render_template("register.html", error=error)


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid email or password."

    return render_template("login.html", error=error)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    records = conn.execute(
        "SELECT * FROM health_records WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    # ✅ Detect high risk properly 
    has_high_risk = any(r["risk"] == "High" for r in records)

    return render_template(
        "dashboard.html",
        records=records,
        has_high_risk=has_high_risk
    )




# ---------- HEALTH FORM ----------
@app.route("/health", methods=["GET", "POST"])
def health():
    if "user_id" not in session:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":
        try:
            age = int(request.form["age"])
            bp = int(request.form["bp"])
            sugar = int(request.form["sugar"])
            smoking = request.form["smoking"]
            family_history = request.form["family_history"]
        except ValueError:
            error = "Please enter valid numeric values."
            return render_template("health.html", error=error)

        # ---------- VALIDATION ----------
        if age < 1 or age > 120:
            error = "Age must be between 1 and 120."
            return render_template("health.html", error=error)

        if bp < 70 or bp > 250:
            error = "Blood pressure must be between 70 and 250 mmHg."
            return render_template("health.html", error=error)

        if sugar < 50 or sugar > 500:
            error = "Blood sugar must be between 50 and 500 mg/dL."
            return render_template("health.html", error=error)

        risk = calculate_risk(age, bp, sugar, smoking, family_history)

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO health_records
            (user_id, age, bp, sugar, smoking, family_history, risk)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            age,
            bp,
            sugar,
            smoking,
            family_history,
            risk
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("health.html", error=error)


# ---------- AWARENESS ----------
@app.route("/awareness")
def awareness():
    return render_template("awareness.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===============================
# START APPLICATION
# ===============================
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)


