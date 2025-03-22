# Create a test admin user directly
from app.db.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_test_admin():
    # Create tables directly
    Base.metadata.create_all(bind=engine)
    
    # Create admin user
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if admin:
            print("Admin user already exists")
            return
            
        admin_user = User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("adminpassword"),
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_admin()