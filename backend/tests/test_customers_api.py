import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.bike import Bike  # Import all models to ensure they are registered with Base
from app.models.ticket import Ticket
from app.models.part import Part
from app.models.ticket_part import TicketPart
from app.models.ticket_update import TicketUpdate
from app.models.service import Service
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

    # Create test customers
    test_customer1 = Customer(
        name="John Doe",
        email="john@example.com",
        phone="123-456-7890",
        notes="Regular customer"
    )

    test_customer2 = Customer(
        name="Jane Smith",
        email="jane@example.com",
        phone="987-654-3210",
        notes="New customer"
    )

    db.add(admin_user)
    db.add(tech_user)
    db.add(test_customer1)
    db.add(test_customer2)
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


def test_create_customer(client: TestClient, admin_token: str):
    new_customer = {
        "name": "New Customer",
        "email": "newcustomer@example.com",
        "phone": "555-123-4567",
        "notes": "Test notes"
    }

    response = client.post(
        "/api/customers/",
        json=new_customer,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_customer["name"]
    assert data["email"] == new_customer["email"]
    assert "id" in data


def test_read_customers(client: TestClient, tech_token: str):
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least the two test customers


def test_read_customer_by_id(client: TestClient, tech_token: str):
    # First, get all customers to find an ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    customers = response.json()
    customer_id = customers[0]["id"]

    # Now get the customer by ID
    response = client.get(
        f"/api/customers/{customer_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id


def test_read_nonexistent_customer(client: TestClient, tech_token: str):
    response = client.get(
        "/api/customers/9999",  # Non-existent ID
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 404


def test_update_customer(client: TestClient, tech_token: str):
    # First, get all customers to find an ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    customers = response.json()
    customer_id = customers[0]["id"]

    # Update the customer
    update_data = {
        "name": "Updated Customer Name",
        "notes": "Updated customer notes"
    }

    response = client.put(
        f"/api/customers/{customer_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["notes"] == update_data["notes"]


def test_search_customers(client: TestClient, tech_token: str):
    # Search by name
    response = client.get(
        "/api/customers/search/?search_term=John",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("John" in customer["name"] for customer in data)


def test_delete_customer(client: TestClient, admin_token: str):
    # Create a customer to delete
    new_customer = {
        "name": "Customer To Delete",
        "email": "todelete@example.com",
        "phone": "111-222-3333",
    }

    response = client.post(
        "/api/customers/",
        json=new_customer,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    customer_id = response.json()["id"]

    # Delete the customer
    response = client.delete(
        f"/api/customers/{customer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

    # Verify the customer no longer exists
    response = client.get(
        f"/api/customers/{customer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


def test_delete_customer_unauthorized(client: TestClient, tech_token: str):
    # First, get all customers to find an ID
    response = client.get(
        "/api/customers/",
        headers={"Authorization": f"Bearer {tech_token}"}
    )
    customers = response.json()
    customer_id = customers[0]["id"]

    # Try to delete the customer with tech user
    response = client.delete(
        f"/api/customers/{customer_id}",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 403  # Forbidden for non-admin users


def test_search_customers_minimum_length(client: TestClient, tech_token: str):
    # Try to search with a single character (should fail)
    response = client.get(
        "/api/customers/search/?search_term=J",
        headers={"Authorization": f"Bearer {tech_token}"}
    )

    assert response.status_code == 422  # Validation error
