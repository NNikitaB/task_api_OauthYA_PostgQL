from .repository import BaseSqlAsyncRepository
from app.models.Users import Users
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(BaseSqlAsyncRepository[Users]):

    def __init__(self, session: AsyncSession):
        super().__init__(session)


    async def activate_user(self, uuid):
        """Activate user"""
        user = await self.get_by_identifier(uuid)
        if user:
            user.is_active = True
            await self.update(user)
            return user
        return None

    async def deactivate_user(self, uuid):
        """Deactivate user"""
        user = await self.get_by_identifier(uuid)
        if user:
            user.is_active = False
            await self.update(user)
            return user
        return None 

    async def get_by_email(self, email):
        """Get user by email"""
        return await self.list(filters={'email': email})
    async def get_by_username(self, username):
        """Get user by username"""
        return await self.list(filters={'username': username})
    async def get_by_phone(self, phone):
        """Get user by phone"""
        return await self.list(filters={'phone': phone})
    async def get_by_psevdonim(self, psevdonim):
        """Get user by psevdonim"""
        return await self.list(filters={'psevdonim': psevdonim})
    async def get_list_services(self, uuid):
        """Get list of services for user"""
        user = await self.get_by_identifier(uuid)
        if user:
            return user.services_access
        return None