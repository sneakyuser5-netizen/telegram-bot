import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(files)")
print(cur.fetchall())

conn.close()

