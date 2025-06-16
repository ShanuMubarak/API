import sqlite3
import os

def init_db():
    db_path = "data/database.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        total_spent REAL,
        total_quantity INTEGER,
        num_orders INTEGER,
        age INTEGER,
        gender_code INTEGER
    )
    """)

    conn.commit()
    conn.close()