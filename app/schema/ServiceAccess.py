from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schema import UserResponse
from uuid import UUID
from app.core import ServiceName, AccessLevel
from datetime import datetime, UTC


class ServiceAccessBase(BaseModel):
    service_name: ServiceName = ServiceName.Default
    is_active: bool = False
    access_level: AccessLevel = AccessLevel.User


class ServiceAccessGet(ServiceAccessBase):
    id: int
    granted_at: Optional[datetime]
    user_uuid: UUID


class ServiceAccessCreate(ServiceAccessBase):
    user_uuid: UUID
    granted_at: Optional[datetime] = datetime.now()


class ServiceAccessUpdate(ServiceAccessBase):
    id: int


class ServiceAccessResponse(ServiceAccessGet):
    pass