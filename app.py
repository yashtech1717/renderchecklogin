from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mikasa_secret_key"


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        login_time TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
    admin = cursor.fetchone()

    if not admin:
        cursor.execute(
            "INSERT INTO users(username,password,login_time) VALUES(?,?,?)",
            ("admin", "1234", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        )

    conn.commit()
    conn.close()


create_table()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password,login_time) VALUES(?,?,?)",
                (
                    username,
                    password,
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                )
            )
            conn.commit()
            flash("Registration Successful")
            return redirect("/login")

        except:
            flash("Username Already Exists")

        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET login_time=? WHERE id=?",
                (
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    user["id"]
                )
            )
            conn.commit()

            session["user"] = username

            if username == "admin" and password == "1234":
                return redirect("/admin")

            return redirect("/dashboard")

        flash("Invalid Username or Password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (session["user"],)
    )

    user = cursor.fetchone()
    conn.close()

    return render_template("user_dashboard.html", user=user)


@app.route("/admin")
def admin():
    if "user" not in session or session["user"] != "admin":
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)