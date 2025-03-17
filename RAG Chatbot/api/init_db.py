import sqlite3

def init_database():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    # Create application_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS application_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_query TEXT,
        gpt_response TEXT,
        model TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create document_store table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS document_store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database() 