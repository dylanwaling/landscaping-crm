
import sqlite3

DB_NAME = "crm.db"

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory
    return conn

def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                notes TEXT,
                gate_code TEXT
            )
        """)
        try:
            c.execute("ALTER TABLE customers ADD COLUMN gate_code TEXT")
        except Exception:
            pass

        c.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                service TEXT,
                date TEXT,
                notes TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        """)
        try:
            c.execute("ALTER TABLE users ADD COLUMN password TEXT")
        except Exception:
            pass

        # Ensure admin user exists
        c.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        if c.fetchone()["count"] == 0:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '1234'))

        conn.commit()
