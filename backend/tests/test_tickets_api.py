import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from main import app
from app.db.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.ticket import Ticket, TicketStatus, TicketPriority
from app.models.ticket_update import TicketUpdate
from app.models.ticket_part import TicketPart
from app.models.part import Part
from app.models.bike import Bike
from app.models.customer import Customer
from app.models.service import Service


client = TestClient(app)


# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Use in-memory database for tests
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
    
    # Create test admin user
    db = TestingSessionLocal()
    admin_user = User(
        email="admin@example.com",
        username="admin",
        full_name="Test Admin",
        hashed_password=get_password_hash("adminpassword"),
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    
    yield db
    
    # Clean up
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_token(test_db):
    """Get an admin token for authentication"""
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword"
    }
    response = client.post("/api/auth/login", data=login_data)
    return response.json()["access_token"]


@pytest.fixture
def test_customer(test_db: Session):
    """Create a test customer"""
    customer = Customer(
        name="Test Customer",
        email="test_customer@example.com",
        phone="555-1234"
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    yield customer
    
    # Cleanup
    test_db.delete(customer)
    test_db.commit()


@pytest.fixture
def test_bike(test_db: Session, test_customer):
    """Create a test bike for the test customer"""
    bike = Bike(
        name="Test Bike",
        specs="Make: Test Make, Model: Test Model, Year: 2022, Serial: TEST12345",
        owner_id=test_customer.id
    )
    test_db.add(bike)
    test_db.commit()
    test_db.refresh(bike)
    yield bike
    
    # Cleanup
    test_db.delete(bike)
    test_db.commit()


@pytest.fixture
def test_part(test_db: Session):
    """Create a test part"""
    part = Part(
        name="Test Part",
        description="Test part description",
        category="Test Category",
        sku="PART-001",
        quantity=10,
        cost_price=50.00,
        retail_price=100.00
    )
    test_db.add(part)
    test_db.commit()
    test_db.refresh(part)
    yield part
    
    # Cleanup
    test_db.delete(part)
    test_db.commit()


@pytest.fixture
def test_service(test_db: Session):
    """Create a test service"""
    service = Service(
        name="Test Service",
        description="Test service description",
        price=75.00
    )
    test_db.add(service)
    test_db.commit()
    test_db.refresh(service)
    yield service
    
    # Cleanup
    test_db.delete(service)
    test_db.commit()


def test_create_ticket(admin_token, test_db: Session, test_bike, test_service):
    """Test creating a new ticket"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    ticket_data = {
        "ticket_number": "T-TEST-001",
        "problem_description": "Test problem description",
        "diagnosis": "Test diagnosis",
        "status": TicketStatus.INTAKE.value,
        "priority": TicketPriority.MEDIUM.value,
        "bike_id": test_bike.id,
        "technician_id": None,
        "labor_cost": 50.00
    }
    
    response = client.post("/api/tickets/", json=ticket_data, headers=headers)
    assert response.status_code == 201
    
    created_ticket = response.json()
    assert created_ticket["ticket_number"] == ticket_data["ticket_number"]
    assert created_ticket["problem_description"] == ticket_data["problem_description"]
    assert created_ticket["status"] == ticket_data["status"]
    
    # Clean up
    test_db.query(TicketUpdate).filter(TicketUpdate.ticket_id == created_ticket["id"]).delete()
    test_db.query(Ticket).filter(Ticket.id == created_ticket["id"]).delete()
    test_db.commit()


def test_get_tickets(admin_token, test_db: Session, test_bike):
    """Test retrieving tickets with optional filtering"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create some test tickets
    ticket1 = Ticket(
        ticket_number="T-TEST-001",
        problem_description="Test problem 1",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.LOW,
        bike_id=test_bike.id
    )
    
    ticket2 = Ticket(
        ticket_number="T-TEST-002",
        problem_description="Test problem 2",
        status=TicketStatus.IN_PROGRESS,
        priority=TicketPriority.HIGH,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket1)
    test_db.add(ticket2)
    test_db.commit()
    test_db.refresh(ticket1)
    test_db.refresh(ticket2)
    
    # Test getting all tickets
    response = client.get("/api/tickets/", headers=headers)
    assert response.status_code == 200
    tickets = response.json()
    assert len(tickets) >= 2
    
    # Test filtering by status
    response = client.get(f"/api/tickets/?status={TicketStatus.INTAKE.value}", headers=headers)
    assert response.status_code == 200
    tickets = response.json()
    assert all(t["status"] == TicketStatus.INTAKE.value for t in tickets)
    
    # Test filtering by priority
    response = client.get(f"/api/tickets/?priority={TicketPriority.HIGH.value}", headers=headers)
    assert response.status_code == 200
    tickets = response.json()
    assert all(t["priority"] == TicketPriority.HIGH.value for t in tickets)
    
    # Test filtering by bike_id
    response = client.get(f"/api/tickets/?bike_id={test_bike.id}", headers=headers)
    assert response.status_code == 200
    tickets = response.json()
    assert all(t["bike_id"] == test_bike.id for t in tickets)
    
    # Clean up
    test_db.query(Ticket).filter(Ticket.id.in_([ticket1.id, ticket2.id])).delete(synchronize_session=False)
    test_db.commit()


def test_get_ticket(admin_token, test_db: Session, test_bike):
    """Test retrieving a specific ticket"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create a test ticket
    ticket = Ticket(
        ticket_number="T-TEST-003",
        problem_description="Test problem description",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.MEDIUM,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket)
    test_db.commit()
    test_db.refresh(ticket)
    
    # Test getting the ticket
    response = client.get(f"/api/tickets/{ticket.id}", headers=headers)
    assert response.status_code == 200
    retrieved_ticket = response.json()
    assert retrieved_ticket["id"] == ticket.id
    assert retrieved_ticket["ticket_number"] == ticket.ticket_number
    
    # Test getting a non-existent ticket
    response = client.get("/api/tickets/99999", headers=headers)
    assert response.status_code == 404
    
    # Clean up
    test_db.query(Ticket).filter(Ticket.id == ticket.id).delete()
    test_db.commit()


def test_update_ticket(admin_token, test_db: Session, test_bike):
    """Test updating a ticket"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create a test ticket
    ticket = Ticket(
        ticket_number="T-TEST-004",
        problem_description="Original description",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.MEDIUM,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket)
    test_db.commit()
    test_db.refresh(ticket)
    
    # Update the ticket
    update_data = {
        "problem_description": "Updated description",
        "status": TicketStatus.IN_PROGRESS.value,
        "priority": TicketPriority.HIGH.value,
        "note": "Status updated to in progress"
    }
    
    response = client.put(f"/api/tickets/{ticket.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_ticket = response.json()
    assert updated_ticket["problem_description"] == update_data["problem_description"]
    assert updated_ticket["status"] == update_data["status"]
    assert updated_ticket["priority"] == update_data["priority"]
    
    # Verify ticket update was created
    updates = test_db.query(TicketUpdate).filter(TicketUpdate.ticket_id == ticket.id).all()
    assert len(updates) > 0
    assert any(u.note == update_data["note"] for u in updates)
    
    # Clean up
    test_db.query(TicketUpdate).filter(TicketUpdate.ticket_id == ticket.id).delete()
    test_db.query(Ticket).filter(Ticket.id == ticket.id).delete()
    test_db.commit()


def test_delete_ticket(admin_token, test_db: Session, test_bike):
    """Test deleting a ticket"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create a test ticket
    ticket = Ticket(
        ticket_number="T-TEST-005",
        problem_description="Test problem to delete",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.MEDIUM,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket)
    test_db.commit()
    test_db.refresh(ticket)
    
    # Delete the ticket
    response = client.delete(f"/api/tickets/{ticket.id}", headers=headers)
    assert response.status_code == 204
    
    # Verify ticket is deleted
    deleted_ticket = test_db.query(Ticket).filter(Ticket.id == ticket.id).first()
    assert deleted_ticket is None


def test_ticket_updates(admin_token, test_db: Session, test_bike):
    """Test ticket updates endpoints"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create a test ticket
    ticket = Ticket(
        ticket_number="T-TEST-006",
        problem_description="Test problem for updates",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.MEDIUM,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket)
    test_db.commit()
    test_db.refresh(ticket)
    
    # Create a ticket update
    update_data = {
        "ticket_id": ticket.id,
        "new_status": TicketStatus.DIAGNOSIS.value,
        "note": "Moving to diagnosis phase",
        "user_id": 1  # Admin user
    }
    
    response = client.post(f"/api/tickets/{ticket.id}/updates", json=update_data, headers=headers)
    assert response.status_code == 201
    created_update = response.json()
    assert created_update["note"] == update_data["note"]
    assert created_update["new_status"] == update_data["new_status"]
    
    # Get ticket updates
    response = client.get(f"/api/tickets/{ticket.id}/updates", headers=headers)
    assert response.status_code == 200
    updates = response.json()
    assert len(updates) >= 1
    
    # Clean up
    test_db.query(TicketUpdate).filter(TicketUpdate.ticket_id == ticket.id).delete()
    test_db.query(Ticket).filter(Ticket.id == ticket.id).delete()
    test_db.commit()


def test_ticket_parts(admin_token, test_db: Session, test_bike, test_part):
    """Test ticket parts endpoints"""
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    
    # Create a test ticket
    ticket = Ticket(
        ticket_number="T-TEST-007",
        problem_description="Test problem for parts",
        status=TicketStatus.INTAKE,
        priority=TicketPriority.MEDIUM,
        bike_id=test_bike.id
    )
    
    test_db.add(ticket)
    test_db.commit()
    test_db.refresh(ticket)
    
    # Add a part to the ticket
    part_data = {
        "ticket_id": ticket.id,
        "part_id": test_part.id,
        "quantity": 2,
        "price_charged": test_part.retail_price
    }
    
    response = client.post(f"/api/tickets/{ticket.id}/parts", json=part_data, headers=headers)
    assert response.status_code == 201
    created_part = response.json()
    assert created_part["part_id"] == part_data["part_id"]
    assert created_part["quantity"] == part_data["quantity"]
    
    # Get ticket parts
    response = client.get(f"/api/tickets/{ticket.id}/parts", headers=headers)
    assert response.status_code == 200
    parts = response.json()
    assert len(parts) == 1
    
    # Update a ticket part
    update_part_data = {
        "quantity": 3,
        "price_charged": 110.00
    }
    
    response = client.put(
        f"/api/tickets/{ticket.id}/parts/{test_part.id}", 
        json=update_part_data, 
        headers=headers
    )
    assert response.status_code == 200
    updated_part = response.json()
    assert updated_part["quantity"] == update_part_data["quantity"]
    assert updated_part["price_charged"] == update_part_data["price_charged"]
    
    # Remove a part from the ticket
    response = client.delete(
        f"/api/tickets/{ticket.id}/parts/{test_part.id}", 
        headers=headers
    )
    assert response.status_code == 204
    
    # Verify part is removed
    response = client.get(f"/api/tickets/{ticket.id}/parts", headers=headers)
    assert response.status_code == 200
    parts = response.json()
    assert len(parts) == 0
    
    # Clean up
    test_db.query(TicketUpdate).filter(TicketUpdate.ticket_id == ticket.id).delete()
    test_db.query(Ticket).filter(Ticket.id == ticket.id).delete()
    test_db.commit()