from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.database.db import get_async_session
from sqlalchemy.future import select
from uuid import UUID,uuid4
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.AudioFiles import AudioFiles
from app.schema.AudioFile import AudioFileResponse
from typing import List


audio_files_router = APIRouter(prefix="/api/v1/audio_files", tags=["AudioFiles"])

AUDIO_STORAGE_PATH = "audio_storage/"


# get random str for filename 
def get_random_str():
    return str(uuid4())




@audio_files_router.post("/", response_model=AudioFileResponse)
async def upload_audio(file: UploadFile = File(...),filename:str = get_random_str(), user_uuid: UUID = uuid4(), db: AsyncSession = Depends(get_async_session)):
    file_location = f"{AUDIO_STORAGE_PATH}{file.filename}"

    audio_file = AudioFiles(
        user_id=user_uuid,
        file_name=file.filename,
        file_path=file_location
    )
    db.add(audio_file)
    await db.commit()
    await db.refresh(audio_file)
    return audio_file

@audio_files_router.get("/", response_model=List[AudioFileResponse])
async def list_audio_files(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(AudioFiles))
    return result.scalars().all()

@audio_files_router.get("/{audio_id}", response_model=AudioFileResponse)
async def get_audio(audio_id: int, db: AsyncSession = Depends(get_async_session)):
    audio_file = await db.get(AudioFiles, audio_id)
    if not audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return audio_file