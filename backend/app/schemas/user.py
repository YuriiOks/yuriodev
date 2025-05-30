from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Schema for creating a user via OAuth (email is primary identifier from provider)
class UserCreateOAuth(UserBase):
    # No password needed for OAuth creation
    # Provider details will be handled by CRUD using arguments from auth callback
    pass

# Schema for traditional user creation (if you add email/password signup)
# class UserCreateTraditional(UserBase):
#     password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None # Allow email change? (consider implications)
    is_active: Optional[bool] = None
    # Add other fields that can be updated

# Properties to return to client
class User(UserBase):
    id: int # Or UUID if using UUIDs
    is_active: bool
    is_superuser: bool
    provider: Optional[str] = None
    # provider_user_id: Optional[str] = None # Usually not exposed to client
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True # Pydantic V1, for V2 use from_attributes = True
        # from_attributes = True # For Pydantic V2

# User properties stored in DB
class UserInDB(User):
    hashed_password: Optional[str] = None
    provider_user_id: Optional[str] = None # Stored in DB but not always sent to client
