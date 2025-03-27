import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.bike import Bike
from main import app


# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Use in-memory database for tests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db_override():
    # Setup: Override the dependency
    original_get_db = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Teardown: Restore original dependency if it existed
    if original_get_db:
        app.dependency_overrides[get_db] = original_get_db
    else:
        del app.dependency_overrides[get_db]


@pytest.fixture()
def test_db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)

    # Create test users and data
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

    # Create test customers
    test_customer1 = Customer(
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        notes="Regular customer"
    )

    # Add test bike
    test_bike = Bike(
        name="Mountain Bike",
        specs="29er hardtail, 1x12 drivetrain",
        owner_id=1  # Will be assigned to customer1
    )

    db.add(admin_user)
    db.add(tech_user)
    db.add(test_customer1)
    db.add(test_bike)
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


def test_create_bike(client: TestClient, admin_token: str, test_db):
    # First get customer ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    customers = response.json()
    customer_id = customers[0]["id"]
    
    new_bike = {
        "name": "Road Bike",
        "specs": "Carbon frame, 22-speed",
        "owner_id": customer_id
    }

    response = client.post(
        "/api/bikes/",
        json=new_bike,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_bike["name"]
    assert data["specs"] == new_bike["specs"]
    assert data["owner_id"] == customer_id
    assert "id" in data


def test_read_bikes(client: TestClient, tech_token: str):
    response = client.get(
        "/api/bikes/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1  # At least one bike should exist


def test_read_bike_by_id(client: TestClient, tech_token: str):
    # First, get all bikes to find an ID
    response = client.get(
        "/api/bikes/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    bikes = response.json()
    bike_id = bikes[0]["id"]

    # Now get the bike by ID
    response = client.get(
        f"/api/bikes/{bike_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == bike_id


def test_read_nonexistent_bike(client: TestClient, tech_token: str):
    response = client.get(
        "/api/bikes/9999",  # Non-existent ID
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 404


def test_update_bike(client: TestClient, tech_token: str):
    # First, get all bikes to find an ID
    response = client.get(
        "/api/bikes/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    bikes = response.json()
    bike_id = bikes[0]["id"]

    # Update the bike
    update_data = {
        "name": "Updated Bike Name",
        "specs": "Updated bike specs"
    }

    response = client.put(
        f"/api/bikes/{bike_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["specs"] == update_data["specs"]


def test_filter_bikes_by_owner(client: TestClient, tech_token: str):
    # Get customers to find an owner ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    customers = response.json()
    owner_id = customers[0]["id"]
    
    # Filter bikes by owner
    response = client.get(
        f"/api/bikes/?owner_id={owner_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(bike["owner_id"] == owner_id for bike in data)


def test_delete_bike(client: TestClient, admin_token: str):
    # Create a bike to delete
    # First get customer ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    customers = response.json()
    customer_id = customers[0]["id"]
    
    new_bike = {
        "name": "Bike To Delete",
        "specs": "Test bike for deletion",
        "owner_id": customer_id
    }

    response = client.post(
        "/api/bikes/",
        json=new_bike,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    bike_id = response.json()["id"]

    # Delete the bike
    response = client.delete(
        f"/api/bikes/{bike_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

    # Verify the bike no longer exists
    response = client.get(
        f"/api/bikes/{bike_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


def test_delete_bike_unauthorized(client: TestClient, tech_token: str):
    # First, get all bikes to find an ID
    response = client.get(
        "/api/bikes/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    bikes = response.json()
    bike_id = bikes[0]["id"]

    # Try to delete the bike with tech user
    response = client.delete(
        f"/api/bikes/{bike_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 403  # Forbidden for non-admin users