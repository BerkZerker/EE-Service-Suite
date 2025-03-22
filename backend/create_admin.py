# Script to create initial admin user
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import argparse

def create_admin_user(db: Session, email: str, username: str, password: str, full_name: str = None):
    # Check if user already exists
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"User with email {email} already exists")
        return None
    
    user = db.query(User).filter(User.username == username).first()
    if user:
        print(f"User with username {username} already exists")
        return None
    
    # Create admin user
    admin_user = User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"Admin user '{username}' created successfully")
    return admin_user

def main():
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--email", required=True, help="Admin email")
    parser.add_argument("--username", required=True, help="Admin username")
    parser.add_argument("--password", required=True, help="Admin password")
    parser.add_argument("--full-name", help="Admin full name")
    
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        create_admin_user(
            db=db,
            email=args.email,
            username=args.username,
            password=args.password,
            full_name=args.full_name
        )
    finally:
        db.close()

if __name__ == "__main__":
    main()