from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import PostgresSettings

settings = PostgresSettings()
engine = create_async_engine(settings.postgres_url, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession)


async def db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
