import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.part import Part
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

    # Add test part
    test_part = Part(
        name="Test Part",
        description="Test part description",
        category="Test Category",
        sku="TEST123",
        quantity=10,
        min_stock=2,
        reorder_point=5,
        cost_price=10.00,
        retail_price=20.00,
    )

    db.add(admin_user)
    db.add(tech_user)
    db.add(test_part)
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


@pytest.fixture
def test_part(test_db):
    # Get the first part from the database (already created in test_db fixture)
    return test_db.query(Part).first()


def test_create_part(client: TestClient, tech_token: str):
    data = {
        "name": "New Test Part",
        "description": "Description of test part",
        "category": "Test",
        "sku": "SKU123",
        "quantity": 5,
        "min_stock": 1,
        "reorder_point": 3,
        "cost_price": 15.50,
        "retail_price": 25.00
    }
    response = client.post(
        "/api/parts/",
        headers={"Authorization": f"Bearer {tech_token}"},
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert content["sku"] == data["sku"]
    assert content["quantity"] == data["quantity"]
    assert content["cost_price"] == data["cost_price"]
    assert content["retail_price"] == data["retail_price"]
    assert round(content["markup"], 2) == 61.29  # (25 - 15.50) / 15.50 * 100


def test_get_part(client: TestClient, tech_token: str, test_part):
    response = client.get(
        f"/api/parts/{test_part.id}",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == test_part.name
    assert content["sku"] == test_part.sku
    assert content["markup"] == 100.0  # (20 - 10) / 10 * 100


def test_get_all_parts(client: TestClient, tech_token: str, test_part):
    response = client.get(
        "/api/parts/",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1
    assert any(part["id"] == test_part.id for part in content)


def test_update_part(client: TestClient, tech_token: str, test_part):
    data = {
        "name": "Updated Test Part",
        "retail_price": 25.00
    }
    response = client.put(
        f"/api/parts/{test_part.id}",
        headers={"Authorization": f"Bearer {tech_token}"},
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["retail_price"] == data["retail_price"]
    assert content["markup"] == 150.0  # (25 - 10) / 10 * 100


def test_delete_part(client: TestClient, admin_token: str, test_db: pytest.fixture):
    # Create a part specifically for deletion to avoid conflicts
    part = Part(
        name="Delete Test Part",
        description="Part to be deleted",
        category="Test",
        sku="DELETE123",
        quantity=10,
        cost_price=5.00,
        retail_price=10.00,
    )
    test_db.add(part)
    test_db.commit()
    test_db.refresh(part)
    
    response = client.delete(
        f"/api/parts/{part.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    
    # Verify part is deleted
    response = client.get(
        f"/api/parts/{part.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404


def test_search_parts(client: TestClient, tech_token: str, test_part):
    response = client.get(
        "/api/parts/search/?search_term=Test",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1
    assert any(part["id"] == test_part.id for part in content)


def test_adjust_stock(client: TestClient, tech_token: str, test_part):
    initial_quantity = test_part.quantity
    
    # Add stock
    response = client.put(
        f"/api/parts/{test_part.id}/adjust-stock?quantity_change=5",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["quantity"] == initial_quantity + 5
    
    # Remove stock
    response = client.put(
        f"/api/parts/{test_part.id}/adjust-stock?quantity_change=-3",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["quantity"] == initial_quantity + 5 - 3
    
    # Try to remove too much stock
    response = client.put(
        f"/api/parts/{test_part.id}/adjust-stock?quantity_change=-20",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 400


def test_get_low_stock_parts(client: TestClient, tech_token: str, test_db):
    # Create a part with quantity below reorder point
    low_stock_part = Part(
        name="Low Stock Part",
        description="Part with low stock",
        category="Test",
        sku="LOWSTOCK123",
        quantity=2,
        min_stock=1,
        reorder_point=5,
        cost_price=5.00,
        retail_price=10.00,
    )
    test_db.add(low_stock_part)
    test_db.commit()
    test_db.refresh(low_stock_part)
    
    response = client.get(
        "/api/parts/low-stock/",
        headers={"Authorization": f"Bearer {tech_token}"},
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1
    assert any(part["id"] == low_stock_part.id for part in content)