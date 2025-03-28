#!/usr/bin/env python
"""
Set up test data for the EE-Service-Suite application.
This script handles:
1. Creating admin user
2. Creating test customers, bikes, parts, and tickets
3. Fixing any enum issues in the database
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta
import random
import argparse

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.abspath("."))

from app.db.database import engine, SessionLocal
from app.core.security import get_password_hash
from app.models.ticket import TicketStatus, TicketPriority

def create_admin_user(conn, cursor):
    """Create a test admin user if it doesn't exist"""
    print("Creating admin user...")
    cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@example.com",))
    admin_id = cursor.fetchone()
    
    if not admin_id:
        now = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO users (email, username, hashed_password, full_name, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "admin@example.com",
            "admin",
            "$2b$12$4ZLqyAFoGCHejWV8qG2zUe0eJXZ35GwHJFTcN1JijRCErfHsZsGC.",  # "adminpassword"
            "Admin User",
            "ADMIN",  # Use uppercase for enum
            1,  # is_active = True
            now,
            now
        ))
        conn.commit()
        print("Admin user created successfully")
        
        cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@example.com",))
        admin_id = cursor.fetchone()[0]
    else:
        admin_id = admin_id[0]
        print("Using existing admin user")
        
    return admin_id

def check_if_data_exists(conn, cursor):
    """Check if we already have test data in the database"""
    cursor.execute("SELECT COUNT(*) FROM tickets")
    ticket_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]
    
    print(f"Found {customer_count} customers and {ticket_count} tickets in database")
    return customer_count > 0 and ticket_count > 0

def create_test_data():
    """Create all test data for the application"""
    print("Initializing test data...")
    
    # Get the database path
    db_path = engine.url.database
    print(f"Using database at: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 0. Check if we need to create data
        if check_if_data_exists(conn, cursor):
            print("Test data already exists. If you want to reset it, use --reset flag.")
            return
        
        print("Creating test data...")
        
        # 1. Create admin user
        admin_id = create_admin_user(conn, cursor)
        
        # 2. Create customers
        print("Creating customers...")
        customer_data = [
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
        
        now = datetime.utcnow().isoformat()
        customer_ids = []
        for customer in customer_data:
            cursor.execute("""
                INSERT INTO customers (name, email, phone, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                customer["name"],
                customer["email"],
                customer["phone"],
                customer["notes"],
                now,
                now
            ))
            conn.commit()
            customer_ids.append(cursor.lastrowid)
        
        # 3. Create bikes for each customer
        print("Creating bikes...")
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
        
        bike_ids = []
        for i, customer_id in enumerate(customer_ids):
            if i < len(bike_specs):
                for bike in bike_specs[i]:
                    cursor.execute("""
                        INSERT INTO bikes (name, specs, owner_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        bike["name"],
                        bike["specs"],
                        customer_id,
                        now,
                        now
                    ))
                    conn.commit()
                    bike_ids.append(cursor.lastrowid)
        
        # 4. Create parts
        print("Creating parts...")
        parts_data = [
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
        
        part_ids = []
        for part in parts_data:
            cursor.execute("""
                INSERT INTO parts (name, description, category, sku, quantity, min_stock, 
                                reorder_point, cost_price, retail_price, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                part["name"],
                part["description"],
                part["category"],
                part["sku"],
                part["quantity"],
                part["min_stock"],
                part["reorder_point"],
                part["cost_price"],
                part["retail_price"],
                now,
                now
            ))
            conn.commit()
            part_ids.append(cursor.lastrowid)
        
        # 5. Create tickets with various statuses - using ENUM names directly
        print("Creating tickets...")
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
        
        # Status values - using ENUM names directly
        statuses = [s.name for s in TicketStatus]
        priorities = [p.name for p in TicketPriority]
        
        for i in range(6):  # Create 6 tickets, one for each status
            # Select a random bike and proper status for this index
            bike_id = random.choice(bike_ids)
            status = statuses[min(i, len(statuses)-1)]
            priority = random.choice(priorities)
            
            # Prepare data that varies by status
            is_early_status = status in ["INTAKE", "DIAGNOSIS"]
            diagnosis = None if is_early_status else random.choice(diagnoses)
            labor_cost = random.choice([45.00, 65.00, 85.00, 120.00])
            
            # Convert dates to strings for SQLite
            created_at = (datetime.utcnow() - timedelta(days=5)).isoformat()
            estimated_completion = (datetime.utcnow() + timedelta(days=random.randint(1, 10))).isoformat()
            
            # Create the ticket
            cursor.execute("""
                INSERT INTO tickets (
                    ticket_number, problem_description, diagnosis, status, priority,
                    estimated_completion, bike_id, technician_id, labor_cost, total_parts_cost,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"T-{2023}{i+1:04d}",
                random.choice(problems),
                diagnosis,
                status,
                priority,
                estimated_completion,
                bike_id,
                admin_id,
                labor_cost,
                0.0,  # We'll update this later
                created_at,
                now
            ))
            conn.commit()
            ticket_id = cursor.lastrowid
            
            # Add status updates to show progression
            status_idx = statuses.index(status)
            for j in range(status_idx + 1):
                update_status = statuses[j]
                update_timestamp = (datetime.utcnow() - timedelta(days=5-j)).isoformat()
                prev_status = statuses[j-1] if j > 0 else None
                
                cursor.execute("""
                    INSERT INTO ticket_updates (
                        ticket_id, previous_status, new_status, note, user_id,
                        timestamp, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ticket_id,
                    prev_status,
                    update_status,
                    f"Updated status to {update_status}",
                    admin_id,
                    update_timestamp,
                    update_timestamp,
                    update_timestamp
                ))
                conn.commit()
            
            # Add parts to tickets that are beyond the intake stage
            if not is_early_status:
                num_parts = random.randint(1, 3)
                selected_part_ids = random.sample(part_ids, num_parts)
                total_parts_cost = 0.0
                
                for part_id in selected_part_ids:
                    # Get the retail price for this part
                    cursor.execute("SELECT retail_price FROM parts WHERE id = ?", (part_id,))
                    retail_price = cursor.fetchone()[0]
                    
                    # Add the part to the ticket
                    quantity = random.randint(1, 2)
                    cursor.execute("""
                        INSERT INTO ticket_parts (
                            ticket_id, part_id, quantity, price_charged, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        ticket_id,
                        part_id,
                        quantity,
                        retail_price,
                        now,
                        now
                    ))
                    conn.commit()
                    
                    total_parts_cost += quantity * retail_price
                
                # Update the ticket's total parts cost
                if total_parts_cost > 0:
                    cursor.execute("""
                        UPDATE tickets SET total_parts_cost = ?
                        WHERE id = ?
                    """, (
                        total_parts_cost,
                        ticket_id
                    ))
                    conn.commit()
        
        print("Test data creation complete!")
    
    except Exception as e:
        print(f"Error creating test data: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def fix_enums():
    """Fix the enum values in the database if needed"""
    print("Checking and fixing enum values if needed...")
    
    # Get the database path
    db_path = engine.url.database
    print(f"Using database at: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if we need to fix enums by looking at ticket status values
        cursor.execute("SELECT DISTINCT status FROM tickets")
        statuses = cursor.fetchall()
        
        # If we don't have any tickets yet, we're done
        if not statuses:
            print("No tickets found. No enum fixes needed.")
            return
            
        print(f"Current ticket statuses: {statuses}")
        
        # If we find lowercase values, we need to fix the enums
        has_lowercase = any(status[0].islower() for status in statuses if status[0])
        
        if not has_lowercase:
            print("Enums already correct. No action needed.")
            return
        
        # Map from lowercase value to uppercase name
        ticket_statuses = {status.value: status.name for status in TicketStatus}
        ticket_priorities = {priority.value: priority.name for priority in TicketPriority}
        
        print("Updating ticket statuses...")
        for status_value, status_name in ticket_statuses.items():
            cursor.execute("UPDATE tickets SET status = ? WHERE status = ?", (status_name, status_value))
            conn.commit()
            print(f"  - Updated '{status_value}' to '{status_name}'")
        
        print("Updating ticket priorities...")
        for priority_value, priority_name in ticket_priorities.items():
            cursor.execute("UPDATE tickets SET priority = ? WHERE priority = ?", (priority_name, priority_value))
            conn.commit()
            print(f"  - Updated '{priority_value}' to '{priority_name}'")
        
        print("Updating ticket update statuses...")
        for status_value, status_name in ticket_statuses.items():
            # Update new_status
            cursor.execute("UPDATE ticket_updates SET new_status = ? WHERE new_status = ?", (status_name, status_value))
            conn.commit()
            print(f"  - Updated new_status '{status_value}' to '{status_name}'")
            
            # Update previous_status
            cursor.execute("UPDATE ticket_updates SET previous_status = ? WHERE previous_status = ?", (status_name, status_value))
            conn.commit()
            print(f"  - Updated previous_status '{status_value}' to '{status_name}'")
        
        print("Enum values fixed successfully!")
    
    except Exception as e:
        print(f"Error fixing enums: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def reset_data():
    """Reset the database by deleting all data from relevant tables"""
    print("Resetting database...")
    
    # Get the database path
    db_path = engine.url.database
    print(f"Using database at: {db_path}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Disable foreign key checks to allow deleting from tables with foreign key constraints
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # List of tables to delete data from (in reverse order of dependencies)
        tables = [
            "ticket_updates",
            "ticket_parts",
            "tickets",
            "parts",
            "bikes",
            "customers",
            # Don't delete users so we keep the admin account
        ]
        
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print(f"Deleted all data from {table}")
        
        # Re-enable foreign key checks
        cursor.execute("PRAGMA foreign_keys = ON")
        
        print("Database reset complete!")
    
    except Exception as e:
        print(f"Error resetting database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='Set up test data for EE Service Suite')
    parser.add_argument('--reset', action='store_true', help='Reset the database before adding test data')
    parser.add_argument('--fix-enums', action='store_true', help='Only fix enum values without adding test data')
    args = parser.parse_args()
    
    if args.reset:
        reset_data()
        
    if args.fix_enums:
        fix_enums()
        return
        
    # Default behavior: create test data and fix enums if needed
    create_test_data()
    fix_enums()

if __name__ == "__main__":
    main()