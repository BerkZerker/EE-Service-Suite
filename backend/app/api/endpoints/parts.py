from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_admin_user, get_current_active_user, get_db
)
from app.models.user import User
from app.models.part import Part
from app.schemas.part import (
    Part as PartSchema,
    PartCreate,
    PartUpdate
)

router = APIRouter()


@router.get(
    "/", 
    response_model=List[PartSchema],
    summary="Get all parts",
    description="Retrieve all parts with pagination and optional filtering by name, category, or SKU."
)
def read_parts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    category: Optional[str] = None,
    sku: Optional[str] = None,
    low_stock: Optional[bool] = False,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all parts with pagination and optional filtering.
    
    Parameters:
    - **skip**: Number of parts to skip (for pagination)
    - **limit**: Maximum number of parts to return (for pagination)
    - **name**: Optional filter by part name (case-insensitive partial match)
    - **category**: Optional filter by part category (case-insensitive partial match)
    - **sku**: Optional filter by SKU (case-insensitive partial match)
    - **low_stock**: Optional filter to show only parts below reorder point
    
    Returns:
    - List of part objects
    """
    query = db.query(Part)

    # Apply filters if provided
    if name:
        query = query.filter(Part.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Part.category.ilike(f"%{category}%"))
    if sku:
        query = query.filter(Part.sku.ilike(f"%{sku}%"))
    if low_stock:
        query = query.filter(Part.quantity <= Part.reorder_point)

    parts = query.offset(skip).limit(limit).all()
    return parts


@router.post(
    "/", 
    response_model=PartSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create part",
    description="Create a new part record."
)
def create_part(
    *,
    db: Session = Depends(get_db),
    part_in: PartCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new part record.
    
    Parameters:
    - **part_in**: Part creation data
    
    Returns:
    - Created part object with ID
    """
    # Check if SKU already exists
    if part_in.sku:
        existing_part = db.query(Part).filter(Part.sku == part_in.sku).first()
        if existing_part:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Part with this SKU already exists",
            )
            
    # Create new part
    part = Part(
        name=part_in.name,
        description=part_in.description,
        category=part_in.category,
        sku=part_in.sku,
        quantity=part_in.quantity,
        min_stock=part_in.min_stock,
        reorder_point=part_in.reorder_point,
        cost_price=part_in.cost_price,
        retail_price=part_in.retail_price,
    )
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


@router.get(
    "/{part_id}", 
    response_model=PartSchema,
    summary="Get part by ID",
    description="Get a specific part by ID."
)
def read_part(
    part_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific part by ID.
    
    Parameters:
    - **part_id**: ID of the part to retrieve
    
    Returns:
    - Part object
    
    Raises:
    - 404: Part not found
    """
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found",
        )
    return part


@router.put(
    "/{part_id}", 
    response_model=PartSchema,
    summary="Update part",
    description="Update a specific part by ID."
)
def update_part(
    *,
    db: Session = Depends(get_db),
    part_id: int,
    part_in: PartUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a specific part by ID.
    
    Parameters:
    - **part_id**: ID of the part to update
    - **part_in**: Part update data
    
    Returns:
    - Updated part object
    
    Raises:
    - 404: Part not found
    - 400: SKU already exists
    """
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found",
        )

    # Check if SKU is being updated and already exists
    if part_in.sku and part_in.sku != part.sku:
        existing_part = db.query(Part).filter(Part.sku == part_in.sku).first()
        if existing_part:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Part with this SKU already exists",
            )

    # Update part fields
    update_data = part_in.model_dump(exclude_unset=True)
    for field in update_data:
        if hasattr(part, field) and update_data[field] is not None:
            setattr(part, field, update_data[field])

    db.add(part)
    db.commit()
    db.refresh(part)
    return part


@router.delete(
    "/{part_id}", 
    response_model=PartSchema,
    summary="Delete part",
    description="Delete a specific part by ID. Only accessible to admin users."
)
def delete_part(
    *,
    db: Session = Depends(get_db),
    part_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a specific part by ID.
    
    Parameters:
    - **part_id**: ID of the part to delete
    
    Returns:
    - Deleted part object
    
    Raises:
    - 404: Part not found
    
    Only accessible to admin users.
    """
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found",
        )

    # Check if part is used in any tickets
    if part.ticket_parts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete part that is used in tickets",
        )

    db.delete(part)
    db.commit()
    return part


@router.get(
    "/search/", 
    response_model=List[PartSchema],
    summary="Search parts",
    description="Search for parts by name, category, or SKU. Requires at least 2 characters in the search term."
)
def search_parts(
    search_term: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Search for parts by name, category, or SKU.
    
    Parameters:
    - **search_term**: Text to search for in part name, category, or SKU (minimum 2 characters)
    
    Returns:
    - List of matching part objects
    
    Raises:
    - 422: Validation error if search term is less than 2 characters
    """
    parts = db.query(Part).filter(
        (Part.name.ilike(f"%{search_term}%")) |
        (Part.category.ilike(f"%{search_term}%")) |
        (Part.sku.ilike(f"%{search_term}%"))
    ).all()

    return parts


@router.put(
    "/{part_id}/adjust-stock", 
    response_model=PartSchema,
    summary="Adjust part stock",
    description="Adjust the stock quantity of a part (add or remove units)."
)
def adjust_stock(
    *,
    db: Session = Depends(get_db),
    part_id: int,
    quantity_change: int = Query(..., description="Quantity to add (positive) or remove (negative)"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Adjust the stock quantity of a part.
    
    Parameters:
    - **part_id**: ID of the part to adjust
    - **quantity_change**: Quantity to add (positive) or remove (negative)
    
    Returns:
    - Updated part object
    
    Raises:
    - 404: Part not found
    - 400: Insufficient stock
    """
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Part not found",
        )
    
    # Check if removing stock would result in negative quantity
    if quantity_change < 0 and abs(quantity_change) > part.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock to remove requested quantity",
        )
    
    part.quantity += quantity_change
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


@router.get(
    "/low-stock/", 
    response_model=List[PartSchema],
    summary="Get low stock parts",
    description="Get all parts that are below their reorder point."
)
def get_low_stock_parts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all parts that are below their reorder point.
    
    Returns:
    - List of parts below reorder point
    """
    parts = db.query(Part).filter(Part.quantity <= Part.reorder_point).all()
    return parts