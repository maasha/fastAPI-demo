from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    """Model for creating a new user"""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    age: int = Field(..., ge=0, le=150, description="User's age")
    address: str = Field(..., min_length=1, max_length=200, description="User's address")


class UserUpdate(BaseModel):
    """Model for updating a user (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    address: Optional[str] = Field(None, min_length=1, max_length=200)


class User(BaseModel):
    """Full user model with ID"""
    id: int = Field(..., description="Unique user ID")
    name: str
    age: int
    address: str
