"""Модуль конфигурации базы данных."""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from typing import AsyncGenerator
from settings import settings
from typing import Any

engine: AsyncEngine = create_async_engine(settings.db.url)

Base: Any = declarative_base()
async_session: sessionmaker = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        yield session
