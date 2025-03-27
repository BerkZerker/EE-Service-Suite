#!/usr/bin/env python
# Add a test user directly through SQLAlchemy with timestamps

import os
import sys
from datetime import datetime
from sqlalchemy import text

sys.path.append(os.path.abspath("."))

from app.db.database import engine, SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def add_test_user():
    db = SessionLocal()
    try:
        # First check if the user already exists
        existing_user = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_user:
            print("Test user already exists")
            return
        
        # Create test user with direct SQL for timestamp columns
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                INSERT INTO users (email, username, hashed_password, full_name, role, is_active, created_at, updated_at)
                VALUES (:email, :username, :password, :full_name, :role, :is_active, :created_at, :updated_at)
                """),
                {
                    "email": "admin@example.com",
                    "username": "admin",
                    "password": get_password_hash("adminpassword"),
                    "full_name": "Admin User",
                    "role": "admin",  # UserRole.ADMIN value
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            )
            conn.commit()
        
        print("Test user created successfully")
    finally:
        db.close()

if __name__ == "__main__":
    add_test_user()