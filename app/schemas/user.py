from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., example="your_secure_password")


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
