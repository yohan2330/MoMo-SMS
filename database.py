import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            phone TEXT,
            amount REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_transaction(db_path, date, phone, amount, category):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (date, phone, amount, category) VALUES (?, ?, ?, ?)',
                   (date, phone, amount, category))
    conn.commit()
    conn.close()