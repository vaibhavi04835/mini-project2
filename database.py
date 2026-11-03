
import sqlite3
import hashlib
import secrets
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "students.db"


def connect():
    return sqlite3.connect(str(DB_PATH))


def initialize_database():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                course TEXT,
                email TEXT,
                phone TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200000
    ).hex()


def register_user(fullname, username, email, password):
    salt = secrets.token_bytes(16)
    hashed = hash_password(password, salt)

    try:
        with connect() as conn:
            conn.execute("""
                INSERT INTO users
                (fullname, username, email, password_hash, salt)
                VALUES (?, ?, ?, ?, ?)
            """, (
                fullname, username, email,
                hashed, salt.hex()
            ))

        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "Username already exists."


def login_user(username, password):
    with connect() as conn:
        user = conn.execute("""
            SELECT id, fullname, password_hash, salt
            FROM users WHERE username=?
        """, (username,)).fetchone()

    if not user:
        return None

    user_id, fullname, saved_hash, salt = user

    entered_hash = hash_password(
        password, bytes.fromhex(salt)
    )

    if secrets.compare_digest(entered_hash, saved_hash):
        return user_id, fullname

    return None


def add_student(user_id, values):
    with connect() as conn:
        conn.execute("""
            INSERT INTO students
            (user_id, name, age, gender, course, email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, *values))


def get_students(user_id, search=""):
    with connect() as conn:
        return conn.execute("""
            SELECT id, name, age, gender, course, email, phone
            FROM students
            WHERE user_id=?
            AND (name LIKE ? OR CAST(id AS TEXT) LIKE ?)
            ORDER BY id DESC
        """, (
            user_id,
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()


def update_student(student_id, user_id, values):
    with connect() as conn:
        conn.execute("""
            UPDATE students
            SET name=?, age=?, gender=?, course=?, email=?, phone=?
            WHERE id=? AND user_id=?
        """, (*values, student_id, user_id))


def delete_student(student_id, user_id):
    with connect() as conn:
        conn.execute("""
            DELETE FROM students
            WHERE id=? AND user_id=?
        """, (student_id, user_id))
