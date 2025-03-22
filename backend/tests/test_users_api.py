import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from main import app


# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create test admin and regular users
    db = TestingSessionLocal()
    admin_user = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpassword"),
        role=UserRole.ADMIN,
        is_active=True
    )
    
    tech_user = User(
        email="tech@example.com",
        username="technician",
        full_name="Tech User",
        hashed_password=get_password_hash("techpassword"),
        role=UserRole.TECHNICIAN,
        is_active=True
    )
    
    db.add(admin_user)
    db.add(tech_user)
    db.commit()
    
    yield db
    
    # Teardown - drop all tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def admin_token(client: TestClient):
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    return response.json()["access_token"]


@pytest.fixture()
def tech_token(client: TestClient):
    login_data = {
        "username": "tech@example.com",
        "password": "techpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    return response.json()["access_token"]


def test_create_user(client: TestClient, admin_token: str):
    new_user = {
        "email": "newuser@example.com",
        "username": "newuser",
        "full_name": "New User",
        "password": "newpassword",
    }
    
    response = client.post(
        "/api/users/",
        json=new_user,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == new_user["email"]
    assert data["username"] == new_user["username"]
    assert "id" in data


def test_create_user_unauthorized(client: TestClient, tech_token: str):
    new_user = {
        "email": "another@example.com",
        "username": "another",
        "full_name": "Another User",
        "password": "anotherpassword",
    }
    
    response = client.post(
        "/api/users/",
        json=new_user,
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403


def test_read_users(client: TestClient, admin_token: str):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least the admin and tech users


def test_read_users_unauthorized(client: TestClient, tech_token: str):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403


def test_read_user_me(client: TestClient, tech_token: str):
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "technician"


def test_update_user_me(client: TestClient, tech_token: str):
    update_data = {
        "full_name": "Updated Tech Name"
    }
    
    response = client.put(
        "/api/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]


def test_read_user_by_id_admin(client: TestClient, admin_token: str):
    # First, get all users to find the tech user's ID
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    users = response.json()
    tech_user = next(user for user in users if user["username"] == "technician")
    
    # Now get the tech user by ID
    response = client.get(
        f"/api/users/{tech_user['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "technician"


def test_read_user_by_id_unauthorized(client: TestClient, tech_token: str):
    # First, get the admin user ID
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    tech_id = response.json()["id"]
    
    # Attempt to access a different user (with ID tech_id + 1 or tech_id - 1)
    other_id = tech_id + 1 if tech_id > 1 else tech_id - 1
    
    response = client.get(
        f"/api/users/{other_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403


def test_update_user_admin(client: TestClient, admin_token: str):
    # First, get all users to find the tech user's ID
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    users = response.json()
    tech_user = next(user for user in users if user["username"] == "technician")
    
    update_data = {
        "full_name": "Admin Updated Name"
    }
    
    response = client.put(
        f"/api/users/{tech_user['id']}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]


def test_update_user_unauthorized(client: TestClient, tech_token: str):
    # First, get the admin user ID
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    tech_id = response.json()["id"]
    
    # Attempt to update a different user
    other_id = tech_id + 1 if tech_id > 1 else tech_id - 1
    
    update_data = {
        "full_name": "Unauthorized Update"
    }
    
    response = client.put(
        f"/api/users/{other_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403


def test_delete_user(client: TestClient, admin_token: str):
    # Create a user to delete
    new_user = {
        "email": "todelete@example.com",
        "username": "todelete",
        "full_name": "To Delete",
        "password": "deletepassword",
    }
    
    response = client.post(
        "/api/users/",
        json=new_user,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    user_id = response.json()["id"]
    
    # Delete the user
    response = client.delete(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    
    # Verify the user no longer exists
    response = client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 404


def test_delete_user_unauthorized(client: TestClient, tech_token: str):
    # First, get the admin user ID
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    tech_id = response.json()["id"]
    
    # Attempt to delete a different user
    other_id = tech_id + 1 if tech_id > 1 else tech_id - 1
    
    response = client.delete(
        f"/api/users/{other_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    
    assert response.status_code == 403