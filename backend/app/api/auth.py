from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse, UserUpdate
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        company_name=user_data.company_name,
        industry=user_data.industry
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": new_user.email, "user_id": new_user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Build user response with safe attribute access
    user_dict = {
        "id": new_user.id,
        "email": new_user.email,
        "company_name": new_user.company_name,
        "industry": new_user.industry,
        "created_at": new_user.created_at,
        "phone": getattr(new_user, 'phone', None),
        "address": getattr(new_user, 'address', None),
        "city": getattr(new_user, 'city', None),
        "state": getattr(new_user, 'state', None),
        "pincode": getattr(new_user, 'pincode', None),
        "gstin": getattr(new_user, 'gstin', None),
        "pan": getattr(new_user, 'pan', None),
        "registration_date": getattr(new_user, 'registration_date', None),
        "company_size": getattr(new_user, 'company_size', None),
        "annual_revenue": getattr(new_user, 'annual_revenue', None)
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Build user response with safe attribute access
    user_dict = {
        "id": user.id,
        "email": user.email,
        "company_name": user.company_name,
        "industry": user.industry,
        "created_at": user.created_at,
        "phone": getattr(user, 'phone', None),
        "address": getattr(user, 'address', None),
        "city": getattr(user, 'city', None),
        "state": getattr(user, 'state', None),
        "pincode": getattr(user, 'pincode', None),
        "gstin": getattr(user, 'gstin', None),
        "pan": getattr(user, 'pan', None),
        "registration_date": getattr(user, 'registration_date', None),
        "company_size": getattr(user, 'company_size', None),
        "annual_revenue": getattr(user, 'annual_revenue', None)
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    profile_data: UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    try:
        # Update user fields
        update_data = profile_data.dict(exclude_unset=True)
        
        print(f"Updating profile for user {current_user.id}")
        print(f"Update data: {update_data}")
        
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        print(f"Profile updated successfully for user {current_user.id}")
        
        return current_user
    except Exception as e:
        db.rollback()
        print(f"Error updating profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )

