from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncGenerator

Base = declarative_base()

engine = create_async_engine('postgresql+asyncpg://postgres:pass@localhost/postgres')
engine.connect()

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session