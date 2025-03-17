from db_utils import get_db_connection

def test_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test document_store
        cursor.execute('SELECT COUNT(*) FROM document_store')
        doc_count = cursor.fetchone()[0]
        print(f"Documents in store: {doc_count}")
        
        # Test application_logs
        cursor.execute('SELECT COUNT(*) FROM application_logs')
        log_count = cursor.fetchone()[0]
        print(f"Log entries: {log_count}")
        
        conn.close()
        print("✅ Database test successful!")
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    test_database() 