from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schema import ServiceAccessGet, ServiceAccessBase
from uuid import UUID
from app.core import UserRole
from datetime import datetime,UTC

class UserBase(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    psevdonim: str
    is_active: bool = True
    is_superuser: bool = False
    role: UserRole = UserRole.USER
    notes: Optional[str] = None
    phone: Optional[str] = None

class UserGet(UserBase):
    email_verified: bool = False
    services_access: List[ServiceAccessBase] 

class UserCreate(UserBase):
    email_verified: bool = False
    services_access: List[ServiceAccessGet] = []
    hashed_password: str
    created_at: datetime = datetime.now(UTC)

class UserUpdate(UserBase):
    hashed_password: str
    email_verified: Optional[bool] = None
    services_access: Optional[List[ServiceAccessGet]] = None

class UserResponse(UserBase):
    created_at: datetime
    email_verified: bool
    services_access: List[ServiceAccessGet] = [] 
