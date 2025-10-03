import sqlite3

DB_FILE = "reminders.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        remind_time TEXT,
        is_important INTEGER,
        status TEXT
    )""")
    conn.commit()
    conn.close()

def add_reminder(message, remind_time, important):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO reminders (message, remind_time, is_important, status) VALUES (?, ?, ?, ?)",
              (message, remind_time, 1 if important else 0, "pending"))
    conn.commit()
    conn.close()
