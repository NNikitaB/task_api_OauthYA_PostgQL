from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_async_session
from app.models.Users import Users
from app.schema.User import UserResponse
from app.services.oauth import OAuthYandex
from app.services.TokenJWT import TokenJWT
from app.logger import logger
from uuid import UUID

oauth_router = APIRouter(prefix="/api/v1/oauth", tags=["Oauth"])



@oauth_router.get("/yandex")
async def login_with_yandex(code: str, db: AsyncSession = Depends(get_async_session)):
    """Авторизация через Яндекс"""
    logger.info(f"Авторизация через Яндекс с кодом: {code}")
    oauth_yandex = OAuthYandex()
    jwt_token = TokenJWT()
    access_token = await oauth_yandex.exchange_code_for_token(code)
    user_data = await oauth_yandex.get_user_info(access_token)
 
    email = user_data.get("email")
    existing_user = await db.execute(select(Users).where(Users.email == email))
    user = existing_user.scalar()

    if not user:
        user = Users(username=user_data.get("login"), email=email, hashed_password="yandex_oauth")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Создан новый пользователь: {user.username}")

    access_token = jwt_token.create_access_token({"sub": str(user.uuid)})
    refresh_token = jwt_token.create_refresh_token({"sub": str(user.uuid)})

    logger.info(f"Выданы токены для пользователя {user.username}")

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@oauth_router.post("/refresh")
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_async_session)):
    """Обновление access_token с помощью refresh_token"""
    jwt_token = TokenJWT()
    user_uuid = jwt_token.verify_refresh_token(refresh_token)
    if not user_uuid:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await db.get(Users, UUID(user_uuid))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = jwt_token.create_access_token({"sub": str(user.uuid)})

    return {"access_token": access_token, "token_type": "bearer"}