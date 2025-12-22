from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow frontend to connect

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- ROUTES ----------

@app.route("/")
def home():
    return {"status": "Backend running successfully 🚀"}

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Validation
    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    if len(message) < 10:
        return jsonify({"error": "Message must be at least 10 characters"}), 400

    # Save to DB
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO contacts (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.now())
    )
    conn.commit()
    conn.close()

    return jsonify({"success": "Message sent successfully ✅"}), 200


@app.route("/messages", methods=["GET"])
def all_messages():
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
    conn.close()

    return jsonify([dict(row) for row in messages])


if __name__ == "__main__":
    app.run(debug=True)
