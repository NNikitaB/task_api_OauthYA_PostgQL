from .repository import BaseSqlAsyncRepository
from app.models.Users import Users


class UsersRepository(BaseSqlAsyncRepository[Users]):
    pass