"""Модуль конфигурации базы данных хранения токенов."""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from settings import settings
from typing import Any

engine: AsyncEngine = create_async_engine(settings.sqlite_db.url)

Base: Any = declarative_base()

AsyncSession: sessionmaker = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

async_session: AsyncSession = AsyncSession()
