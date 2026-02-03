from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    industry: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    company_name: str
    industry: Optional[str] = None
    created_at: datetime
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    registration_date: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[str] = None
    
    class Config:
        from_attributes = True
        # Allow population by field name and ignore extra fields
        populate_by_name = True

class UserUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    registration_date: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

