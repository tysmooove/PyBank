##############################################################################
# auth.py
# Handles user registration and login with SHA-256 password hashing.
##############################################################################

# Imports
import hashlib
import sqlite3
from database import get_connection


# Functions
def hash_password(password):
    """Return SHA-256 hash of the given password string."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """
    Register a new user. Returns True on success, False if username is taken.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    """
    Verify credentials against the database.
    Returns user dict on success, None on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None
