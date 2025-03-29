from fastapi import APIRouter
from .oauth.auth import oauth_router
from .oauth.user import user_router
from .oauth.audio_file import audio_files_router


routers = APIRouter()


routers.include_router(oauth_router)
routers.include_router(user_router)
routers.include_router(audio_files_router)

