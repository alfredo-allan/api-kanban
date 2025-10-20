from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


# Schema base de usuário
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)


# Schema para criar usuário
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


# Schema para atualizar usuário
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=100)


# Schema de resposta do usuário (sem senha)
class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema para login
class UserLogin(BaseModel):
    username: str
    password: str


# Schema de resposta do token
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Schema de dados do token
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None
