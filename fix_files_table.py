import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

try:
    cur.execute("PRAGMA table_info(files)")
    cols = cur.fetchall()

    print("FILES TABLE COLUMNS:")
    for c in cols:
        print(c)

except Exception as e:
    print("ERROR:", e)

conn.close()