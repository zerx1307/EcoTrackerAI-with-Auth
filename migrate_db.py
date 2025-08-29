"""
Database migration script to add OAuth columns to User table
"""
import sqlite3
import os

def migrate_database():
    db_path = 'instance/ecotrack.db'
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add missing columns
        new_columns = [
            ('email', 'VARCHAR(120)'),
            ('name', 'VARCHAR(100)'),
            ('oauth_provider', 'VARCHAR(50)'),
            ('oauth_id', 'VARCHAR(100)')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
                    print(f"Added column: {col_name}")
                except sqlite3.Error as e:
                    print(f"Error adding column {col_name}: {e}")
        
        # Make password_hash nullable by recreating table
        cursor.execute("PRAGMA table_info(user)")
        columns_info = cursor.fetchall()
        
        # Create new table with correct schema
        cursor.execute("""
            CREATE TABLE user_new (
                id INTEGER PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255),
                email VARCHAR(120) UNIQUE,
                name VARCHAR(100),
                oauth_provider VARCHAR(50),
                oauth_id VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Copy data from old table
        cursor.execute("""
            INSERT INTO user_new (id, username, password_hash, email, name, oauth_provider, oauth_id, created_at)
            SELECT id, username, password_hash, email, name, oauth_provider, oauth_id, created_at FROM user
        """)
        
        # Drop old table and rename new one
        cursor.execute("DROP TABLE user")
        cursor.execute("ALTER TABLE user_new RENAME TO user")
        
        conn.commit()
        print("Database migration completed successfully!")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Migration error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
