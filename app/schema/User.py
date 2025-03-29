from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schema.AudioFile import AudioFileResponse
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    uuid: UUID
    is_active: bool
    audio_files: List[AudioFileResponse] = []

    class ConfigDict:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
