from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.deps import (
    get_current_admin_user, get_current_active_user, get_db
)
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get(
    "/", 
    response_model=List[UserSchema], 
    summary="Get all users",
    description="Retrieve all users with pagination. Only accessible to admin users."
)
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Retrieve all users with pagination.
    
    Parameters:
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (for pagination)
    
    Returns:
    - List of user objects
    
    Only accessible to admin users.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post(
    "/", 
    response_model=UserSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Create a new user account. Only accessible to admin users."
)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Create a new user account.
    
    Parameters:
    - **user_in**: User creation data including email, username, password, full_name, and role
    
    Returns:
    - Created user object
    
    Raises:
    - 400: Email or username already exists
    
    Only accessible to admin users.
    """
    # Check if user with this email or username already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists",
        )

    # Create new user
    user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        role=user_in.role,
        hashed_password=security.get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get(
    "/me", 
    response_model=UserSchema,
    summary="Get current user",
    description="Get current authenticated user's profile information."
)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current authenticated user's profile information.
    
    Returns:
    - Current user object
    """
    return current_user


@router.put(
    "/me", 
    response_model=UserSchema,
    summary="Update current user",
    description="Update current authenticated user's profile information."
)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current authenticated user's profile information.
    
    Parameters:
    - **user_in**: User update data which may include email, username, password, full_name
    
    Returns:
    - Updated user object
    
    Raises:
    - 400: Email or username already exists
    """
    # Check if updating to an existing email/username
    if user_in.email and user_in.email != current_user.email:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists",
            )

    if user_in.username and user_in.username != current_user.username:
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists",
            )

    # Update user fields
    user_data = current_user.__dict__

    if user_in.password:
        hashed_password = security.get_password_hash(user_in.password)
        user_in_data = user_in.model_dump(exclude_unset=True)
        user_in_data["hashed_password"] = hashed_password

        # Remove password from the update data
        if "password" in user_in_data:
            del user_in_data["password"]
    else:
        user_in_data = user_in.model_dump(exclude_unset=True)

    for field in user_in_data:
        if field in user_data and user_in_data[field] is not None:
            setattr(current_user, field, user_in_data[field])

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get(
    "/{user_id}", 
    response_model=UserSchema,
    summary="Get user by ID",
    description="Get a specific user by ID. Regular users can only access their own profile, while admin users can access any user profile."
)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by ID.
    
    Parameters:
    - **user_id**: ID of the user to retrieve
    
    Returns:
    - User object
    
    Raises:
    - 403: Not enough permissions (if regular user tries to access another user's profile)
    - 404: User not found
    
    Regular users can only access their own profile.
    Admin users can access any user profile.
    """
    # Check permissions first - non-admin users can only access their own
    # profile
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Then check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put(
    "/{user_id}", 
    response_model=UserSchema,
    summary="Update user by ID",
    description="Update a specific user by ID. Only accessible to admin users."
)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Update a specific user by ID.
    
    Parameters:
    - **user_id**: ID of the user to update
    - **user_in**: User update data which may include email, username, password, full_name, role, is_active
    
    Returns:
    - Updated user object
    
    Raises:
    - 400: Email or username already exists
    - 404: User not found
    
    Only accessible to admin users.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if updating to an existing email/username
    if user_in.email and user_in.email != user.email:
        user_exists = db.query(User).filter(
            User.email == user_in.email).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists",
            )

    if user_in.username and user_in.username != user.username:
        user_exists = db.query(User).filter(
            User.username == user_in.username).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists",
            )

    # Update user fields
    user_data = user.__dict__

    if user_in.password:
        hashed_password = security.get_password_hash(user_in.password)
        user_in_data = user_in.model_dump(exclude_unset=True)
        user_in_data["hashed_password"] = hashed_password

        # Remove password from the update data
        if "password" in user_in_data:
            del user_in_data["password"]
    else:
        user_in_data = user_in.model_dump(exclude_unset=True)

    for field in user_in_data:
        if field in user_data and user_in_data[field] is not None:
            setattr(user, field, user_in_data[field])

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/{user_id}", 
    response_model=UserSchema,
    summary="Delete user",
    description="Delete a specific user by ID. Only accessible to admin users. Cannot delete own account."
)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a specific user by ID.
    
    Parameters:
    - **user_id**: ID of the user to delete
    
    Returns:
    - Deleted user object
    
    Raises:
    - 400: Cannot delete own user account
    - 404: User not found
    
    Only accessible to admin users.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Prevent deleting self
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete own user account",
        )

    db.delete(user)
    db.commit()
    return user
