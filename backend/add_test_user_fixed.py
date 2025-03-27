#!/usr/bin/env python
# Add a test user directly through SQLite with proper timestamps and enum values

import datetime
import os
import sys
import sqlite3

# Add the project root to the Python path
sys.path.append(os.path.abspath("."))

from app.core.security import get_password_hash

def add_test_user():
    """Create a test admin user directly in the SQLite database"""
    
    # Path to the SQLite database
    db_path = "/app/app.db"
    
    # Get the actual path to the database (it might be in a different location in Docker)
    try:
        import sqlalchemy
        from app.db.database import engine
        db_path = engine.url.database
        print(f"Using database at: {db_path}")
    except Exception as e:
        print(f"Could not get database path from SQLAlchemy: {e}")
        print(f"Falling back to default path: {db_path}")
    
    # Create a secure password hash
    password = "adminpassword"
    # We need to generate a hash that will work with the verify_password function
    # This is a bcrypt compatible hash (pre-generated)
    hashed_password = "$2b$12$4ZLqyAFoGCHejWV8qG2zUe0eJXZ35GwHJFTcN1JijRCErfHsZsGC."  # for "adminpassword"
    
    # Current timestamp for created_at and updated_at
    now = datetime.datetime.utcnow().isoformat()
    
    try:
        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@example.com",))
        if cursor.fetchone():
            print("Test user already exists, updating password...")
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE email = ?", 
                (hashed_password, "admin@example.com")
            )
        else:
            # Insert the user directly - using correct enum value 'ADMIN'
            cursor.execute("""
                INSERT INTO users (
                    email, username, hashed_password, full_name, 
                    role, is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "admin@example.com", "admin", hashed_password, "Admin User",
                "ADMIN", 1, now, now
            ))
        
        conn.commit()
        print("Test user created/updated successfully")
        return True
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_test_user()