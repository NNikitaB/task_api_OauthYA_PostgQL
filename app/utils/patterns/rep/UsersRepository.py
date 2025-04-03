from .repository import BaseSqlAsyncRepository
from app.models.Users import Users
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(BaseSqlAsyncRepository[Users]):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    