from database import db

def add_file(category, size, file_id):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM files WHERE category=?",
        (category,)
    )

    cur.execute(
        "INSERT INTO files(category,size,file_id) VALUES(?,?,?)",
        (category,size,file_id)
    )

    conn.commit()
    conn.close()

def get_file(category):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT file_id
        FROM files
        WHERE category=?
        LIMIT 1
        """,
        (category,)
    )

    row = cur.fetchone()

    conn.close()

    return row[0] if row else None


def search_files(keyword):
    """
    Search for files by keyword (partial, case-insensitive match on category).
    
    Args:
        keyword (str): Search keyword
        
    Returns:
        list: List of tuples (category, file_id, size) matching the keyword
    """
    conn = db()
    cur = conn.cursor()

    cur.execute(
        "SELECT category, file_id, size FROM files WHERE LOWER(category) LIKE ? ORDER BY category",
        (f"%{keyword.lower()}%",)
    )

    results = cur.fetchall()
    conn.close()

    return results


def list_categories():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT category
        FROM files
        ORDER BY category
    """)

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]

def delete_file(category):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM files WHERE category=?",
        (category,)
    )

    deleted = cur.rowcount

    conn.commit()
    conn.close()

    return deleted

def list_files_info():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT category,size,created_at
        FROM files
        ORDER BY category
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def record_download(category):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO downloads(category,count)
        VALUES(?,1)
        ON CONFLICT(category)
        DO UPDATE SET count=count+1
        """,
        (category,)
    )

    conn.commit()
    conn.close()


def get_download_stats():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT category,count
        FROM downloads
        ORDER BY count DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
