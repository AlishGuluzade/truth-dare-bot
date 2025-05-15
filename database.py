import sqlite3
from datetime import datetime

DB_NAME = "bot.db"

# ✅ CREATES DATABASES AND TABLES
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # users cədvəli
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            bot_user_id TEXT UNIQUE
        )
    ''')

    # answers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_user_id TEXT,
            question_type TEXT,
            answered_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ✅ CREATE USER IF IT DOES NOT EXIST, RETURN IF IT DOES
def get_or_create_user(telegram_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Find existing user
    c.execute('SELECT bot_user_id FROM users WHERE telegram_id = ?', (telegram_id,))
    row = c.fetchone()

    if row:
        bot_user_id = row[0]
    else:
        # Find the last bot_user_id
        c.execute("SELECT bot_user_id FROM users ORDER BY id DESC LIMIT 1")
        last_row = c.fetchone()
        if last_row:
            last_id = int(last_row[0].split("-")[1])
            next_id = f"USR-{last_id + 1}"
        else:
            next_id = "USR-1001"

        # Add new user
        c.execute('''
            INSERT INTO users (telegram_id, username, bot_user_id)
            VALUES (?, ?, ?)
        ''', (telegram_id, username, next_id))
        bot_user_id = next_id

    conn.commit()
    conn.close()
    return bot_user_id

# ✅ WRITE THE ANSWER
def save_answer(bot_user_id, question_type):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO answers (bot_user_id, question_type, answered_at)
        VALUES (?, ?, ?)
    ''', (bot_user_id, question_type, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
