from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin_user, get_current_active_user, get_db
from app.models.user import User
from app.models.bike import Bike
from app.models.customer import Customer
from app.schemas.bike import Bike as BikeSchema, BikeCreate, BikeUpdate, BikeWithTickets

router = APIRouter()


@router.get(
    "/", 
    response_model=List[BikeSchema],
    summary="Get all bikes",
    description="Retrieve all bikes with pagination and optional filtering by owner ID or name."
)
def read_bikes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all bikes with pagination and optional filtering.
    
    Parameters:
    - **skip**: Number of bikes to skip (for pagination)
    - **limit**: Maximum number of bikes to return (for pagination)
    - **owner_id**: Optional filter by customer/owner ID
    - **name**: Optional filter by bike name (case-insensitive partial match)
    
    Returns:
    - List of bike objects
    """
    query = db.query(Bike)
    
    # Apply filters if provided
    if owner_id:
        query = query.filter(Bike.owner_id == owner_id)
    if name:
        query = query.filter(Bike.name.ilike(f"%{name}%"))
        
    bikes = query.offset(skip).limit(limit).all()
    return bikes


@router.post(
    "/", 
    response_model=BikeSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create bike",
    description="Create a new bike record associated with an existing customer."
)
def create_bike(
    *,
    db: Session = Depends(get_db),
    bike_in: BikeCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new bike record.
    
    Parameters:
    - **bike_in**: Bike creation data including name, specs, and owner_id
    
    Returns:
    - Created bike object with ID
    
    Raises:
    - 404: If the specified customer/owner does not exist
    """
    # Verify owner exists
    owner = db.query(Customer).filter(Customer.id == bike_in.owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    bike = Bike(
        name=bike_in.name,
        specs=bike_in.specs,
        owner_id=bike_in.owner_id
    )
    
    db.add(bike)
    db.commit()
    db.refresh(bike)
    return bike


@router.get(
    "/{bike_id}", 
    response_model=BikeSchema,
    summary="Get bike by ID",
    description="Get a specific bike by ID."
)
def read_bike(
    bike_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific bike by ID.
    
    Parameters:
    - **bike_id**: ID of the bike to retrieve
    
    Returns:
    - Bike object
    
    Raises:
    - 404: Bike not found
    """
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    return bike


@router.get(
    "/{bike_id}/with-tickets", 
    response_model=BikeWithTickets,
    summary="Get bike with tickets",
    description="Get a specific bike with its associated service tickets."
)
def read_bike_with_tickets(
    bike_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific bike with its associated service tickets.
    
    Parameters:
    - **bike_id**: ID of the bike to retrieve
    
    Returns:
    - Bike object with tickets list
    
    Raises:
    - 404: Bike not found
    """
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    return bike


@router.put(
    "/{bike_id}", 
    response_model=BikeSchema,
    summary="Update bike",
    description="Update a specific bike by ID."
)
def update_bike(
    *,
    db: Session = Depends(get_db),
    bike_id: int,
    bike_in: BikeUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a specific bike by ID.
    
    Parameters:
    - **bike_id**: ID of the bike to update
    - **bike_in**: Bike update data which may include name, specs, owner_id
    
    Returns:
    - Updated bike object
    
    Raises:
    - 404: Bike not found
    - 404: Customer not found (if changing owner_id to a non-existent customer)
    """
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    
    # Check owner exists if changing owner
    if bike_in.owner_id is not None:
        owner = db.query(Customer).filter(Customer.id == bike_in.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
    
    update_data = bike_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(bike, field, update_data[field])
    
    db.add(bike)
    db.commit()
    db.refresh(bike)
    return bike


@router.delete(
    "/{bike_id}", 
    response_model=BikeSchema,
    summary="Delete bike",
    description="Delete a specific bike by ID. Only accessible to admin users."
)
def delete_bike(
    *,
    db: Session = Depends(get_db),
    bike_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a specific bike by ID.
    
    Parameters:
    - **bike_id**: ID of the bike to delete
    
    Returns:
    - Deleted bike object
    
    Raises:
    - 404: Bike not found
    
    Only accessible to admin users.
    """
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bike not found",
        )
    
    db.delete(bike)
    db.commit()
    return bike