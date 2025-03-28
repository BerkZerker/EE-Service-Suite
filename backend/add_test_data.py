#!/usr/bin/env python
# Add test data including customers, bikes, tickets, parts, and updates

import os
import sys
from datetime import datetime, timedelta
import random
from sqlalchemy import text

sys.path.append(os.path.abspath("."))

from app.db.database import engine, SessionLocal
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.bike import Bike
from app.models.part import Part
from app.models.ticket import Ticket, TicketStatus, TicketPriority
from app.models.ticket_part import TicketPart
from app.models.ticket_update import TicketUpdate
from app.core.security import get_password_hash

def create_test_user():
    """Create a test admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if the user already exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            # Using direct SQL for the timestamp columns
            with engine.connect() as conn:
                now = datetime.utcnow()
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
                        "role": "admin",  # Using the raw string value from UserRole.ADMIN.value
                        "is_active": True,
                        "created_at": now,
                        "updated_at": now
                    }
                )
                conn.commit()
            
            admin_user = db.query(User).filter(User.email == "admin@example.com").first()
            print("Created admin user")
        return admin_user
    finally:
        db.close()

def create_test_customers():
    """Create test customers"""
    db = SessionLocal()
    try:
        customers = []
        
        # Only create customers if none exist
        if db.query(Customer).count() == 0:
            test_customers = [
                {
                    "name": "John Smith",
                    "email": "john.smith@example.com",
                    "phone": "555-123-4567",
                    "notes": "Regular customer, prefers weekend appointments"
                },
                {
                    "name": "Jane Doe",
                    "email": "jane.doe@example.com",
                    "phone": "555-987-6543",
                    "notes": "New customer, referred by John Smith"
                },
                {
                    "name": "Michael Johnson",
                    "email": "michael.j@example.com",
                    "phone": "555-567-8901",
                    "notes": "Competitive cyclist, very particular about components"
                }
            ]
            
            now = datetime.utcnow()
            # Use direct SQL to avoid timestamp issues
            with engine.connect() as conn:
                for customer_data in test_customers:
                    result = conn.execute(
                        text("""
                        INSERT INTO customers (name, email, phone, notes, created_at, updated_at)
                        VALUES (:name, :email, :phone, :notes, :created_at, :updated_at)
                        RETURNING id
                        """),
                        {
                            **customer_data,
                            "created_at": now,
                            "updated_at": now
                        }
                    )
                    customer_id = result.fetchone()[0]
                    conn.commit()
                    
                    # Get the actual customer object
                    customer = db.query(Customer).filter(Customer.id == customer_id).first()
                    customers.append(customer)
            
            print(f"Created {len(customers)} test customers")
        else:
            customers = db.query(Customer).all()
            print(f"Using {len(customers)} existing customers")
        
        return customers
    finally:
        db.close()

def create_test_bikes(customers):
    """Create test bikes for customers"""
    db = SessionLocal()
    try:
        bikes = []
        
        # Only create bikes if none exist
        if db.query(Bike).count() == 0:
            # Bike specs for different customers
            bike_specs = [
                # For first customer
                [
                    {
                        "name": "Trek Domane SL 5",
                        "specs": "Road bike, Carbon frame, 2022 model, Blue, Serial: TD5-12345"
                    },
                    {
                        "name": "Specialized Rockhopper",
                        "specs": "Mountain bike, Aluminum frame, 2019 model, Red, Serial: SR-67890"
                    }
                ],
                # For second customer
                [
                    {
                        "name": "Cannondale Topstone",
                        "specs": "Gravel bike, Carbon frame, 2021 model, Green, Serial: CT-24680"
                    }
                ],
                # For third customer
                [
                    {
                        "name": "Specialized S-Works Tarmac",
                        "specs": "Road bike, Carbon frame, 2023 model, Black, Serial: SWT-13579"
                    },
                    {
                        "name": "Santa Cruz Hightower",
                        "specs": "Mountain bike, Carbon frame, 2022 model, Orange, Serial: SCH-86420"
                    }
                ]
            ]
            
            now = datetime.utcnow()
            # Use direct SQL to avoid timestamp issues
            with engine.connect() as conn:
                for i, customer in enumerate(customers):
                    if i < len(bike_specs):
                        for bike_data in bike_specs[i]:
                            result = conn.execute(
                                text("""
                                INSERT INTO bikes (name, specs, owner_id, created_at, updated_at)
                                VALUES (:name, :specs, :owner_id, :created_at, :updated_at)
                                RETURNING id
                                """),
                                {
                                    **bike_data,
                                    "owner_id": customer.id,
                                    "created_at": now,
                                    "updated_at": now
                                }
                            )
                            bike_id = result.fetchone()[0]
                            conn.commit()
                            
                            # Get the actual bike object
                            bike = db.query(Bike).filter(Bike.id == bike_id).first()
                            bikes.append(bike)
            
            print(f"Created {len(bikes)} test bikes")
        else:
            bikes = db.query(Bike).all()
            print(f"Using {len(bikes)} existing bikes")
        
        return bikes
    finally:
        db.close()

def create_test_parts():
    """Create test parts"""
    db = SessionLocal()
    try:
        parts = []
        
        # Only create parts if none exist
        if db.query(Part).count() == 0:
            test_parts = [
                {
                    "name": "Continental GP 5000 Tire",
                    "description": "High-performance road tire, 700x25c",
                    "category": "Tires",
                    "sku": "CGP5-700-25",
                    "quantity": 15,
                    "min_stock": 5,
                    "reorder_point": 8,
                    "cost_price": 45.00,
                    "retail_price": 69.99
                },
                {
                    "name": "Shimano 105 Rear Derailleur",
                    "description": "11-speed rear derailleur, medium cage",
                    "category": "Drivetrain",
                    "sku": "S105-RD-M",
                    "quantity": 8,
                    "min_stock": 3,
                    "reorder_point": 5,
                    "cost_price": 52.00,
                    "retail_price": 89.99
                },
                {
                    "name": "SRAM RED Chainring",
                    "description": "53T, 130 BCD, 11-speed compatible",
                    "category": "Drivetrain",
                    "sku": "SR-CR-53",
                    "quantity": 6,
                    "min_stock": 2,
                    "reorder_point": 4,
                    "cost_price": 78.00,
                    "retail_price": 129.99
                },
                {
                    "name": "Maxxis Minion DHF Tire",
                    "description": "29x2.5, 3C compound, tubeless ready",
                    "category": "Tires",
                    "sku": "MM-DHF-29",
                    "quantity": 12,
                    "min_stock": 4,
                    "reorder_point": 6,
                    "cost_price": 38.00,
                    "retail_price": 64.99
                },
                {
                    "name": "Park Tool Chain Cleaner",
                    "description": "CM-5.3 Cyclone Chain Scrubber",
                    "category": "Tools",
                    "sku": "PT-CM5",
                    "quantity": 10,
                    "min_stock": 3,
                    "reorder_point": 5,
                    "cost_price": 17.00,
                    "retail_price": 34.99
                },
                {
                    "name": "Shimano Brake Cable Set",
                    "description": "Road bike brake cable and housing set",
                    "category": "Brakes",
                    "sku": "S-BCS-R",
                    "quantity": 20,
                    "min_stock": 8,
                    "reorder_point": 12,
                    "cost_price": 12.00,
                    "retail_price": 24.99
                }
            ]
            
            now = datetime.utcnow()
            # Use direct SQL to avoid timestamp issues
            with engine.connect() as conn:
                for part_data in test_parts:
                    result = conn.execute(
                        text("""
                        INSERT INTO parts (name, description, category, sku, quantity, min_stock, reorder_point, cost_price, retail_price, created_at, updated_at)
                        VALUES (:name, :description, :category, :sku, :quantity, :min_stock, :reorder_point, :cost_price, :retail_price, :created_at, :updated_at)
                        RETURNING id
                        """),
                        {
                            **part_data,
                            "created_at": now,
                            "updated_at": now
                        }
                    )
                    part_id = result.fetchone()[0]
                    conn.commit()
                    
                    # Get the actual part object
                    part = db.query(Part).filter(Part.id == part_id).first()
                    parts.append(part)
            
            print(f"Created {len(parts)} test parts")
        else:
            parts = db.query(Part).all()
            print(f"Using {len(parts)} existing parts")
        
        return parts
    finally:
        db.close()

def create_test_tickets(bikes, parts, admin_user):
    """Create test tickets with parts and updates"""
    db = SessionLocal()
    try:
        # Only create tickets if none exist
        if db.query(Ticket).count() == 0:
            # Sample problem descriptions and diagnoses
            problems = [
                "Shifting issues with the rear derailleur",
                "Brakes squeaking when applied",
                "Flat tire, needs replacement",
                "Bike tune-up and full service",
                "Headset feels loose, makes noise when turning",
                "Chain skipping under load",
                "Worn brake pads need replacement"
            ]
            
            diagnoses = [
                "Cable tension needs adjustment, derailleur hanger slightly bent",
                "Brake pads contaminated with oil, need cleaning/replacement",
                "Puncture from glass, tire has multiple cuts and should be replaced",
                "General maintenance, chain shows 75% wear, cables frayed",
                "Headset bearings worn, needs rebuild with new bearings",
                "Chain stretch at 0.75, cassette showing wear patterns",
                "Brake pads worn below minimum line, rotors need truing"
            ]
            
            # Create 5 test tickets with various statuses
            tickets = []
            statuses = list(TicketStatus)
            priorities = list(TicketPriority)
            now = datetime.utcnow()
            
            with engine.connect() as conn:
                for i in range(5):
                    # Select a random bike and status
                    bike = random.choice(bikes)
                    status_idx = min(i, len(statuses)-1)  # Ensure we have at least one of each status in order
                    status = statuses[status_idx]
                    priority = random.choice(priorities)
                    
                    estimated_completion = now + timedelta(days=random.randint(1, 14))
                    diagnosis = random.choice(diagnoses) if status.value != "intake" else None
                    labor_cost = random.choice([45.00, 65.00, 85.00, 120.00])
                    
                    # Create the ticket with direct SQL
                    result = conn.execute(
                        text("""
                        INSERT INTO tickets (
                            ticket_number, problem_description, diagnosis, status, priority,
                            estimated_completion, bike_id, technician_id, labor_cost, total_parts_cost, 
                            created_at, updated_at
                        ) VALUES (
                            :ticket_number, :problem_description, :diagnosis, :status, :priority,
                            :estimated_completion, :bike_id, :technician_id, :labor_cost, :total_parts_cost, 
                            :created_at, :updated_at
                        ) RETURNING id
                        """),
                        {
                            "ticket_number": f"T-{2023}{i+1:04d}",
                            "problem_description": random.choice(problems),
                            "diagnosis": diagnosis,
                            "status": status.value,
                            "priority": priority.value,
                            "estimated_completion": estimated_completion,
                            "bike_id": bike.id,
                            "technician_id": admin_user.id,
                            "labor_cost": labor_cost,
                            "total_parts_cost": 0.0,  # Will update this later
                            "created_at": now - timedelta(days=5),  # Create in the past
                            "updated_at": now
                        }
                    )
                    ticket_id = result.fetchone()[0]
                    conn.commit()
                    
                    # Get the actual ticket object
                    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
                    tickets.append(ticket)
                    
                    # Add status updates
                    for j in range(status_idx + 1):
                        update_timestamp = now - timedelta(days=5-j)  # Older updates first
                        previous_status = statuses[j-1].value if j > 0 else None
                        
                        conn.execute(
                            text("""
                            INSERT INTO ticket_updates (
                                ticket_id, previous_status, new_status, note, user_id, 
                                timestamp, created_at, updated_at
                            ) VALUES (
                                :ticket_id, :previous_status, :new_status, :note, :user_id, 
                                :timestamp, :created_at, :updated_at
                            )
                            """),
                            {
                                "ticket_id": ticket_id,
                                "previous_status": previous_status,
                                "new_status": statuses[j].value,
                                "note": f"Updated status to {statuses[j].value}",
                                "user_id": admin_user.id,
                                "timestamp": update_timestamp,
                                "created_at": update_timestamp,
                                "updated_at": update_timestamp
                            }
                        )
                        conn.commit()
                    
                    # Add random parts to tickets (except intake tickets)
                    if status.value != "intake":
                        num_parts = random.randint(1, 3)
                        selected_parts = random.sample(parts, num_parts)
                        total_parts_cost = 0.0
                        
                        for part in selected_parts:
                            quantity = random.randint(1, 2)
                            price_charged = part.retail_price
                            
                            conn.execute(
                                text("""
                                INSERT INTO ticket_parts (
                                    ticket_id, part_id, quantity, price_charged, created_at, updated_at
                                ) VALUES (
                                    :ticket_id, :part_id, :quantity, :price_charged, :created_at, :updated_at
                                )
                                """),
                                {
                                    "ticket_id": ticket_id,
                                    "part_id": part.id,
                                    "quantity": quantity,
                                    "price_charged": price_charged,
                                    "created_at": now,
                                    "updated_at": now
                                }
                            )
                            conn.commit()
                            
                            # Update the ticket's total parts cost
                            total_parts_cost += quantity * price_charged
                        
                        # Update the ticket's total parts cost
                        conn.execute(
                            text("""
                            UPDATE tickets SET total_parts_cost = :total_parts_cost 
                            WHERE id = :ticket_id
                            """),
                            {
                                "total_parts_cost": total_parts_cost,
                                "ticket_id": ticket_id
                            }
                        )
                        conn.commit()
            
            print(f"Created {len(tickets)} test tickets with parts and status updates")
            return tickets
        else:
            tickets = db.query(Ticket).all()
            print(f"Using {len(tickets)} existing tickets")
            return tickets
    finally:
        db.close()

def main():
    """Add all test data to the database"""
    print("Creating test data...")
    
    # Create in proper order to establish relationships
    admin_user = create_test_user()
    customers = create_test_customers()
    bikes = create_test_bikes(customers)
    parts = create_test_parts()
    tickets = create_test_tickets(bikes, parts, admin_user)
    
    print("Test data creation complete!")

if __name__ == "__main__":
    main()