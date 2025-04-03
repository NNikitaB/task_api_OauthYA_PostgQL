from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()
