from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_admin_user, get_current_active_user, get_db
)
from app.models.user import User
from app.models.ticket import Ticket, TicketStatus, TicketPriority
from app.models.ticket_update import TicketUpdate
from app.models.ticket_part import TicketPart
from app.schemas.ticket import (
    Ticket as TicketSchema,
    TicketCreate,
    TicketUpdate as TicketUpdateSchema,
    TicketWithDetails,
    TicketArchiveRequest
)
from app.schemas.ticket_update import (
    TicketUpdateCreate, 
    TicketUpdate as TicketUpdateResponseSchema
)
from app.schemas.ticket_part import (
    TicketPartCreate,
    TicketPartUpdate,
    TicketPart as TicketPartSchema
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[TicketSchema],
    summary="Get all tickets",
    description="Retrieve all tickets with pagination and optional filtering."
)
def read_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    customer_id: Optional[int] = None,
    bike_id: Optional[int] = None,
    technician_id: Optional[int] = None,
    archived: Optional[bool] = False,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve all tickets with pagination and optional filtering.
    
    Parameters:
    - **skip**: Number of tickets to skip (for pagination)
    - **limit**: Maximum number of tickets to return (for pagination)
    - **status**: Optional filter by ticket status
    - **priority**: Optional filter by priority level
    - **customer_id**: Optional filter by customer ID
    - **bike_id**: Optional filter by bike ID
    - **technician_id**: Optional filter by assigned technician ID
    - **archived**: Filter for archived tickets (True) or active tickets (False, default)
    
    Returns:
    - List of ticket objects
    """
    query = db.query(Ticket)

    # Apply filters if provided
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if customer_id:
        query = query.filter(Ticket.bike.has(customer_id=customer_id))
    if bike_id:
        query = query.filter(Ticket.bike_id == bike_id)
    if technician_id:
        query = query.filter(Ticket.technician_id == technician_id)
    
    # Filter by archive status
    query = query.filter(Ticket.is_archived == archived)

    tickets = query.offset(skip).limit(limit).all()
    return tickets


@router.post(
    "/",
    response_model=TicketSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create ticket",
    description="Create a new service ticket."
)
def create_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_in: TicketCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new service ticket.
    
    Parameters:
    - **ticket_in**: Ticket creation data
    
    Returns:
    - Created ticket object with ID
    """
    # Generate a unique ticket number if not provided
    if not hasattr(ticket_in, 'ticket_number') or not ticket_in.ticket_number:
        # Generate a unique ticket number (e.g., "T-001")
        last_ticket = db.query(Ticket).order_by(Ticket.id.desc()).first()
        next_id = 1 if not last_ticket else last_ticket.id + 1
        ticket_number = f"T-{next_id:04d}"
    else:
        ticket_number = ticket_in.ticket_number

    ticket = Ticket(
        ticket_number=ticket_number,
        problem_description=ticket_in.problem_description,
        diagnosis=ticket_in.diagnosis,
        status=ticket_in.status,
        priority=ticket_in.priority,
        estimated_completion=ticket_in.estimated_completion,
        bike_id=ticket_in.bike_id,
        technician_id=ticket_in.technician_id,
        labor_cost=ticket_in.labor_cost
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # Create initial ticket update to log creation
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note="Ticket created",
        user_id=current_user.id
    )
    db.add(ticket_update)
    db.commit()
    
    return ticket


@router.get(
    "/{ticket_id}",
    response_model=TicketWithDetails,
    summary="Get ticket by ID",
    description="Get a specific ticket by ID with all details including updates and parts."
)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific ticket by ID with all details.
    
    Parameters:
    - **ticket_id**: ID of the ticket to retrieve
    
    Returns:
    - Ticket object with updates and parts
    
    Raises:
    - 404: Ticket not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketSchema,
    summary="Update ticket",
    description="Update a specific ticket by ID."
)
def update_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    ticket_in: TicketUpdateSchema,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a specific ticket by ID.
    
    Parameters:
    - **ticket_id**: ID of the ticket to update
    - **ticket_in**: Ticket update data
    
    Returns:
    - Updated ticket object
    
    Raises:
    - 404: Ticket not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    previous_status = ticket.status
    
    # Update ticket fields
    update_data = ticket_in.model_dump(exclude_unset=True)
    for field in update_data:
        if hasattr(ticket, field) and update_data[field] is not None:
            setattr(ticket, field, update_data[field])

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # Add update record if status changed or note provided
    if ticket.status != previous_status or (update_data.get('note') is not None):
        ticket_update = TicketUpdate(
            ticket_id=ticket.id,
            previous_status=previous_status if ticket.status != previous_status else None,
            new_status=ticket.status,
            note=update_data.get('note'),
            user_id=current_user.id
        )
        db.add(ticket_update)
        db.commit()
    
    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete ticket",
    description="Delete a specific ticket by ID. Only accessible to admin users."
)
def delete_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> None:
    """
    Delete a specific ticket by ID.
    
    Parameters:
    - **ticket_id**: ID of the ticket to delete
    
    Raises:
    - 404: Ticket not found
    
    Only accessible to admin users.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    db.delete(ticket)
    db.commit()
    return None


@router.patch(
    "/{ticket_id}/archive",
    response_model=TicketSchema,
    summary="Archive ticket",
    description="Archive a specific ticket by ID."
)
def archive_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    archive_data: TicketArchiveRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Archive a specific ticket by ID.
    
    Parameters:
    - **ticket_id**: ID of the ticket to archive
    - **archive_data**: Optional note to add with the archive action
    
    Returns:
    - Updated ticket object
    
    Raises:
    - 404: Ticket not found
    - 400: Ticket is already archived
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    if ticket.is_archived:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is already archived",
        )
    
    # Update ticket
    ticket.is_archived = True
    db.add(ticket)
    
    # Add ticket update record
    note = archive_data.note if archive_data.note else "Ticket archived"
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note=note,
        user_id=current_user.id
    )
    db.add(ticket_update)
    
    db.commit()
    db.refresh(ticket)
    
    return ticket


@router.patch(
    "/{ticket_id}/unarchive",
    response_model=TicketSchema,
    summary="Unarchive ticket",
    description="Restore a previously archived ticket."
)
def unarchive_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    archive_data: TicketArchiveRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Restore a previously archived ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket to unarchive
    - **archive_data**: Optional note to add with the unarchive action
    
    Returns:
    - Updated ticket object
    
    Raises:
    - 404: Ticket not found
    - 400: Ticket is not archived
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    if not ticket.is_archived:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is not archived",
        )
    
    # Update ticket
    ticket.is_archived = False
    db.add(ticket)
    
    # Add ticket update record
    note = archive_data.note if archive_data.note else "Ticket restored from archive"
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note=note,
        user_id=current_user.id
    )
    db.add(ticket_update)
    
    db.commit()
    db.refresh(ticket)
    
    return ticket


# Ticket Updates Endpoints

@router.get(
    "/{ticket_id}/updates",
    response_model=List[TicketUpdateResponseSchema],
    summary="Get ticket updates",
    description="Get all updates for a specific ticket."
)
def read_ticket_updates(
    ticket_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all updates for a specific ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    - **skip**: Number of updates to skip
    - **limit**: Maximum number of updates to return
    
    Returns:
    - List of ticket update objects
    
    Raises:
    - 404: Ticket not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    updates = db.query(TicketUpdate).filter(
        TicketUpdate.ticket_id == ticket_id
    ).order_by(TicketUpdate.timestamp.desc()).offset(skip).limit(limit).all()
    
    return updates


@router.post(
    "/{ticket_id}/updates",
    response_model=TicketUpdateResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add ticket update",
    description="Add a new update to a ticket."
)
def create_ticket_update(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    update_in: TicketUpdateCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Add a new update to a ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    - **update_in**: Update data including status and note
    
    Returns:
    - Created update object
    
    Raises:
    - 404: Ticket not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Override ticket_id in input to ensure consistency
    update_data = update_in.model_dump()
    update_data["ticket_id"] = ticket_id
    update_data["user_id"] = current_user.id
    
    # Save previous status if changing status
    if "new_status" in update_data and update_data["new_status"] != ticket.status:
        update_data["previous_status"] = ticket.status
        
        # Update the ticket's status
        ticket.status = update_data["new_status"]
        db.add(ticket)
    
    ticket_update = TicketUpdate(**update_data)
    db.add(ticket_update)
    db.commit()
    db.refresh(ticket_update)
    
    return ticket_update


# Ticket Parts Endpoints

@router.get(
    "/{ticket_id}/parts",
    response_model=List[TicketPartSchema],
    summary="Get ticket parts",
    description="Get all parts associated with a specific ticket."
)
def read_ticket_parts(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all parts associated with a specific ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    
    Returns:
    - List of ticket part objects with part details
    
    Raises:
    - 404: Ticket not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    ticket_parts = db.query(TicketPart).filter(
        TicketPart.ticket_id == ticket_id
    ).all()
    
    return ticket_parts


@router.post(
    "/{ticket_id}/parts",
    response_model=TicketPartSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add part to ticket",
    description="Add a part to a specific ticket."
)
def add_ticket_part(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    part_in: TicketPartCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Add a part to a specific ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    - **part_in**: Part data including part_id, quantity, and price
    
    Returns:
    - Created ticket part object
    
    Raises:
    - 404: Ticket not found or Part not found
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Override ticket_id in input to ensure consistency
    part_data = part_in.model_dump()
    part_data["ticket_id"] = ticket_id
    
    ticket_part = TicketPart(**part_data)
    db.add(ticket_part)
    
    # Update the ticket's total parts cost
    ticket.total_parts_cost = ticket.total_parts_cost + ticket_part.calculate_total()
    db.add(ticket)
    
    # Add update about adding part
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note=f"Added {ticket_part.quantity} x part #{ticket_part.part_id}",
        user_id=current_user.id
    )
    db.add(ticket_update)
    
    db.commit()
    db.refresh(ticket_part)
    
    return ticket_part


@router.put(
    "/{ticket_id}/parts/{part_id}",
    response_model=TicketPartSchema,
    summary="Update ticket part",
    description="Update a part associated with a specific ticket."
)
def update_ticket_part(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    part_id: int,
    part_in: TicketPartUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a part associated with a specific ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    - **part_id**: ID of the part
    - **part_in**: Part update data (quantity and/or price)
    
    Returns:
    - Updated ticket part object
    
    Raises:
    - 404: Ticket part not found
    """
    ticket_part = db.query(TicketPart).filter(
        TicketPart.ticket_id == ticket_id,
        TicketPart.part_id == part_id
    ).first()
    
    if not ticket_part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket part not found",
        )
    
    # Calculate current total before update
    old_total = ticket_part.calculate_total()
    
    # Update ticket part fields
    update_data = part_in.model_dump(exclude_unset=True)
    for field in update_data:
        if hasattr(ticket_part, field) and update_data[field] is not None:
            setattr(ticket_part, field, update_data[field])
    
    db.add(ticket_part)
    
    # Calculate new total after update
    new_total = ticket_part.calculate_total()
    
    # Update the ticket's total parts cost
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    ticket.total_parts_cost = ticket.total_parts_cost - old_total + new_total
    db.add(ticket)
    
    # Add update about updating part
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note=f"Updated part #{part_id} details",
        user_id=current_user.id
    )
    db.add(ticket_update)
    
    db.commit()
    db.refresh(ticket_part)
    
    return ticket_part


@router.delete(
    "/{ticket_id}/parts/{part_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove part from ticket",
    description="Remove a part from a specific ticket."
)
def remove_ticket_part(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    part_id: int,
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Remove a part from a specific ticket.
    
    Parameters:
    - **ticket_id**: ID of the ticket
    - **part_id**: ID of the part
    
    Raises:
    - 404: Ticket part not found
    """
    ticket_part = db.query(TicketPart).filter(
        TicketPart.ticket_id == ticket_id,
        TicketPart.part_id == part_id
    ).first()
    
    if not ticket_part:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket part not found",
        )
    
    # Calculate total before removal
    removed_total = ticket_part.calculate_total()
    
    # Update the ticket's total parts cost
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    ticket.total_parts_cost = ticket.total_parts_cost - removed_total
    db.add(ticket)
    
    # Add update about removing part
    ticket_update = TicketUpdate(
        ticket_id=ticket.id,
        new_status=ticket.status,
        note=f"Removed part #{part_id}",
        user_id=current_user.id
    )
    db.add(ticket_update)
    
    # Remove the ticket part
    db.delete(ticket_part)
    db.commit()
    
    return None