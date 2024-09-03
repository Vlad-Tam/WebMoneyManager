from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from currency_service.src.infrastructure.config.db_config import db_config


class DatabaseRepository:
    DATABASE_URL = db_config.get_db_url()
    engine = create_async_engine(DATABASE_URL)
    a_sessionmaker = async_sessionmaker(engine)


database_repository = DatabaseRepository()


async def get_session() -> AsyncSession:
    async with database_repository.a_sessionmaker() as session:
        yield session
