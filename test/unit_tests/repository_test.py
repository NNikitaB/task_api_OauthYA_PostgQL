import pytest
import pytest_asyncio
from sqlalchemy import create_mock_engine,create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,AsyncSession
from sqlalchemy.orm import Session
from app.models.Base import Base
from app.core import UserRole,AccessLevel,ServiceName
from app.models import Users, ServicesAccess
from app.utils.patterns import UsersRepository, ServicesAccessRepository
from app.schema import (
    User,
    UserCreate,
    UserUpdate,
    UserGet,
    ServiceAccessCreate,
    ServiceAccessUpdate,
    ServiceAccessGet,
    ServiceAccessResponse,
)
from typing import Sequence
import datetime
import uuid
import asyncio
from sqlalchemy import event

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


@pytest_asyncio.fixture(scope="function")
async def db_session():
    url="sqlite+aiosqlite://"
    engine = create_async_engine(url=url,echo=True)
    event.listen(engine, 'connect', _fk_pragma_on_connect)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.mark.asyncio
async def test_add_wallet_repos(db_session):
    rep = WalletRepository(db_session)  
    wallet_uuid = await rep.create_wallet()  
    print(f'wallet uuid: {wallet_uuid}')
    assert wallet_uuid is not None


@pytest.mark.asyncio
async def test_get_wallet_repos(db_session):
    rep = WalletRepository(db_session)
    wallet_uuid = await rep.create_wallet()
    assert wallet_uuid is not None
    wallet = await rep.get_wallet(wallet_uuid)
    assert wallet is not None
    print(wallet.model_dump_json())

@pytest.mark.asyncio
async def test_update_wallet_repos(db_session):
    rep = WalletRepository(db_session)
    wallet_uuid = await rep.create_wallet()
    assert wallet_uuid is not None
    wallet = await rep.update_wallet(WalletUpdateSchema(uuid=wallet_uuid,amount=1000))
    assert wallet is not None
    assert wallet.amount == 1000
    print(wallet.model_dump_json())

@pytest.mark.asyncio
async def test_delete_wallet_repos(db_session):
    rep = WalletRepository(db_session)
    wallet_uuid = await rep.create_wallet()
    assert wallet_uuid is not None
    await rep.delete_wallet(uuid=wallet_uuid)
    with pytest.raises(WalletNotCreatedExeption):
        wallet = await rep.get_wallet(wallet_uuid)

@pytest.mark.asyncio    
async def test_get_all_wallet_repos(db_session):
    rep = WalletRepository(db_session)
    #create 10 wallets
    for i in range(10):
        await rep.create_wallet()
    wallets: Sequence[WalletGetSchema] | None = await rep.get_all_wallets()
    assert wallets is not None
    print([w.model_dump_json() for w in wallets])


