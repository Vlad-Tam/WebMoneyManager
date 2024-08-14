from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.db.db_config import DB_HOST, DB_USER, DB_NAME, DB_PORT, DB_PASS

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
)

session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_async(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_async(Base.metadata.delete_all)
