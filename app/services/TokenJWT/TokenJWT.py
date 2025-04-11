from datetime import datetime, timedelta, UTC

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
from app.schema import UserBase,UserGet,ServiceAccessBase
from jose import JWTError, jwt
from app.config import settings

from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenJWT:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict):
        """Создание access токена"""
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict):
        """Создание refresh токена"""
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_refresh_token(self, token: str):
        """Проверка refresh токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_uuid: str|None = payload.get("sub") 
            if user_uuid is None:
                return None
            return user_uuid
        except JWTError:
            return None
        
    def create_user_access_services_tokens(self, user_base: UserGet)-> tuple[str, str]:
        """
            Create access and refresh tokens for a user with service access details.
        
            Args:
                user_base (UserGet): User information containing service access and profile details.
        
            Returns:
                tuple[str, str]: A tuple containing the access token and refresh token.
        
            The method generates two JWT tokens:
            1. An access token with service access levels and user UUID
            2. A refresh token with user profile information
            """
        
        to_encode = {}
        services = [it.model_dump() for it in user_base.services_access]
        to_encode.update({"services": services})
        sub = {"uuid": str(user_base.uuid)}
        to_encode.update({"sub": sub})
        expire1 = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire1})
        access_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        user_data = {
            "sub": str(user_base.uuid),
            "username": user_base.username,
            "psevdonim": user_base.psevdonim, 
            "is_active": user_base.is_active,
            "role": user_base.role
            }
        expire2 = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)
        user_data.update({"exp": expire2})
        refresh_token = jwt.encode(user_data, self.secret_key, algorithm=self.algorithm)
        
        return access_token, refresh_token
    
    def verify_user_refresh_token(self, token: str):
        """Проверка refresh токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_uuid: str|None = payload.get("sub")
            if user_uuid is None:
                return None
            return user_uuid
        except JWTError:
            return None
        
    def verify_user_access_token_get_services(self, token: str)->list[ServiceAccessBase]|None:
        """Проверка access токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_uuid: str|None = payload.get("sub")
            if user_uuid is None:
                return None
            servs: list|None = payload.get("services")
            if servs is None:
                return None
            services: list[ServiceAccessBase] = [ServiceAccessBase(**it) for it in servs]
            return services
        except JWTError:
            return None
    


    
    def verify_access_token(self, token: str):
        """Проверка access токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_uuid: str|None = payload.get("sub")
            if user_uuid is None:
                return None
            return user_uuid
        except JWTError:
            return None

 # = Depends(oauth2_scheme),       
async def get_current_user(token: str, db: AsyncSession = Depends(get_async_session)):
    """Получение текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_uuid: str|None = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(Users, UUID(user_uuid))
    if user is None:
        raise credentials_exception
    return user