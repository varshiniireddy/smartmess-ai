"""
User Authentication & Database Management Module
Uses SQLite with secure password hashing (Werkzeug / SHA-256 with salt)
Supports role-based authorization: 'Mess Manager' and 'Kitchen Staff'
"""

import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "users.db")


def get_db_connection():
    """Returns connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes users table and seeds default demo accounts."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Kitchen Staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Pre-seed default demo users if database is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        demo_users = [
            ("manager", "manager@hostel.edu", "manager123", "Mess Manager"),
            ("cook", "kitchen@hostel.edu", "cook123", "Kitchen Staff")
        ]
        for username, email, password, role in demo_users:
            p_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (username, email, p_hash, role)
            )
        conn.commit()
        print("Initialized SQLite database with demo accounts: 'manager' & 'cook'")

    conn.close()


def register_user(username, email, password, role="Kitchen Staff"):
    """Registers a new user with hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing username or email
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "message": "Username or email is already registered."}

    password_hash = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {
            "success": True,
            "user": {
                "id": user_id,
                "username": username,
                "email": email,
                "role": role
            }
        }
    except Exception as e:
        conn.close()
        return {"success": False, "message": str(e)}


def authenticate_user(username_or_email, password):
    """Authenticates user against SQLite database using hashed passwords."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, password_hash, role FROM users WHERE username = ? OR email = ?",
        (username_or_email, username_or_email)
    )
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    return {"success": False, "message": "Invalid username or password."}


# Initialize DB on module load
init_db()
