from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_admin_user, get_current_active_user, get_db
)
from app.models.user import User
from app.models.customer import Customer
from app.schemas.customer import (
    Customer as CustomerSchema,
    CustomerCreate,
    CustomerUpdate,
    CustomerWithBikes
)

router = APIRouter()


@router.get(
    "/", 
    response_model=List[CustomerSchema],
    summary="Get all customers",
    description="Retrieve all customers with pagination and optional filtering by name, email, or phone."
)
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all customers with pagination and optional filtering.
    
    Parameters:
    - **skip**: Number of customers to skip (for pagination)
    - **limit**: Maximum number of customers to return (for pagination)
    - **name**: Optional filter by customer name (case-insensitive partial match)
    - **email**: Optional filter by customer email (case-insensitive partial match)
    - **phone**: Optional filter by customer phone (case-insensitive partial match)
    
    Returns:
    - List of customer objects
    """
    query = db.query(Customer)

    # Apply filters if provided
    if name:
        query = query.filter(Customer.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Customer.email.ilike(f"%{email}%"))
    if phone:
        query = query.filter(Customer.phone.ilike(f"%{phone}%"))

    customers = query.offset(skip).limit(limit).all()
    return customers


@router.post(
    "/", 
    response_model=CustomerSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create customer",
    description="Create a new customer record."
)
def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: CustomerCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new customer record.
    
    Parameters:
    - **customer_in**: Customer creation data including name, email, phone, and notes
    
    Returns:
    - Created customer object with ID
    """
    customer = Customer(
        name=customer_in.name,
        email=customer_in.email,
        phone=customer_in.phone,
        notes=customer_in.notes,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get(
    "/{customer_id}", 
    response_model=CustomerSchema,
    summary="Get customer by ID",
    description="Get a specific customer by ID."
)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific customer by ID.
    
    Parameters:
    - **customer_id**: ID of the customer to retrieve
    
    Returns:
    - Customer object
    
    Raises:
    - 404: Customer not found
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


@router.get(
    "/{customer_id}/with-bikes", 
    response_model=CustomerWithBikes,
    summary="Get customer with bikes",
    description="Get a specific customer with their associated bikes."
)
def read_customer_with_bikes(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific customer with their associated bikes.
    
    Parameters:
    - **customer_id**: ID of the customer to retrieve
    
    Returns:
    - Customer object with bikes list
    
    Raises:
    - 404: Customer not found
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


@router.put(
    "/{customer_id}", 
    response_model=CustomerSchema,
    summary="Update customer",
    description="Update a specific customer by ID."
)
def update_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    customer_in: CustomerUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a specific customer by ID.
    
    Parameters:
    - **customer_id**: ID of the customer to update
    - **customer_in**: Customer update data which may include name, email, phone, notes
    
    Returns:
    - Updated customer object
    
    Raises:
    - 404: Customer not found
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # Update customer fields
    update_data = customer_in.model_dump(exclude_unset=True)
    for field in update_data:
        if hasattr(customer, field) and update_data[field] is not None:
            setattr(customer, field, update_data[field])

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.delete(
    "/{customer_id}", 
    response_model=CustomerSchema,
    summary="Delete customer",
    description="Delete a specific customer by ID. Only accessible to admin users."
)
def delete_customer(
    *,
    db: Session = Depends(get_db),
    customer_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a specific customer by ID.
    
    Parameters:
    - **customer_id**: ID of the customer to delete
    
    Returns:
    - Deleted customer object
    
    Raises:
    - 404: Customer not found
    
    Only accessible to admin users.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()
    return customer


@router.get(
    "/search/", 
    response_model=List[CustomerSchema],
    summary="Search customers",
    description="Search for customers by name, email, or phone. Requires at least 2 characters in the search term."
)
def search_customers(
    search_term: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Search for customers by name, email, or phone.
    
    Parameters:
    - **search_term**: Text to search for in customer name, email, or phone (minimum 2 characters)
    
    Returns:
    - List of matching customer objects
    
    Raises:
    - 422: Validation error if search term is less than 2 characters
    """
    customers = db.query(Customer).filter(
        (Customer.name.ilike(f"%{search_term}%")) |
        (Customer.email.ilike(f"%{search_term}%")) |
        (Customer.phone.ilike(f"%{search_term}%"))
    ).all()

    return customers