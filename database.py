import sqlite3

DB = "database.db"

def db():
    return sqlite3.connect(DB)

def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id TEXT PRIMARY KEY,
        referrals INTEGER DEFAULT 0,
        referred_by TEXT,
        reward_unlocked INTEGER DEFAULT 0,
        joined_at TEXT
    )
    """)

    cur.execute("""
CREATE TABLE IF NOT EXISTS downloads(
    category TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0
)
""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        size TEXT,
        file_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("FILES TABLE RECREATED")
    conn.commit()
    conn.close()