import sqlite3

def init_db():
    conn = sqlite3.connect("data/knowledge.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT,
            extracted_text TEXT,
            links TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(image_name, extracted_text, links, category):
    conn = sqlite3.connect("data/knowledge.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO knowledge (image_name, extracted_text, links, category)
        VALUES (?, ?, ?, ?)
    ''', (image_name, extracted_text, ", ".join(links), category))
    conn.commit()
    conn.close()
