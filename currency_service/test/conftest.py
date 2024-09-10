import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from currency_service.src.infrastructure.config.db_config import db_config_test
from currency_service.src.infrastructure.models.base import Base
# from currency_service.src.main import app


class DatabaseRepositoryTest:
    DATABASE_URL_TEST = db_config_test.get_db_test_url()
    engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
    a_sessionmaker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


database_repository_test = DatabaseRepositoryTest()


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with DatabaseRepositoryTest.engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with DatabaseRepositoryTest.engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test/currency") as ac:
#         yield ac
