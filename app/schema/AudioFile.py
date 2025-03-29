from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AudioFileBase(BaseModel):
    file_name: str

class AudioFileCreate(AudioFileBase):
    file_path: str

class AudioFileResponse(AudioFileBase):
    id: int
    file_path: str
    user_uuid: UUID

    class ConfigDict:
        from_attributes = True
