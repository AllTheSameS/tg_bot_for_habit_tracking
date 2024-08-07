from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from settings import settings

engine = create_async_engine(settings.db.url)

Base = declarative_base()
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
