import os
import sqlite3

def verify_setup():
    # Check ChromaDB directory
    if os.path.exists("chroma_db"):
        print("✅ ChromaDB directory exists")
    else:
        print("❌ ChromaDB directory missing")
        
    # Check SQLite database
    try:
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        
        # Check document_store table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='document_store'")
        if cursor.fetchone():
            print("✅ document_store table exists")
        else:
            print("❌ document_store table missing")
            
        # Check application_logs table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='application_logs'")
        if cursor.fetchone():
            print("✅ application_logs table exists")
        else:
            print("❌ application_logs table missing")
            
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    verify_setup() 