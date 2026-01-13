from telegram_bot.sqlite_db.sql_database import Base
from sqlalchemy import Column, String, Integer
from telegram_bot.sqlite_db.sql_database import async_session
from sqlalchemy import select


class UserToken(Base):
    """
    Таблица для хранения токена пользователя.

    Attributes:
        id: ID.
        telegram_id: Телеграм ID.
        access_token: Токен.
    """

    __tablename__ = "user_tokens"

    id: Column[Integer] = Column(Integer, primary_key=True)
    telegram_id: Column[Integer] = Column(Integer, nullable=False, unique=True)
    access_token: Column[String] = Column(String, nullable=False)

    @classmethod
    async def get_user_token(cls, telegram_id: int):
        """
        Метод выводящий токен пользователя.
        """

        token = await async_session.execute(
            select(cls).where(cls.telegram_id == telegram_id)
        )

        return token.scalar()

    @classmethod
    async def delete_user_token(cls, telegram_id: int):
        """
        Метод удаления токена пользователя.
        """
        token = await async_session.execute(
            select(cls).where(cls.telegram_id == telegram_id)
        )
        token_obj = token.scalar_one_or_none()

        if token_obj:
            await async_session.delete(token_obj)
            await async_session.commit()
