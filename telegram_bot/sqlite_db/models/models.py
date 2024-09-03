from telegram_bot.sqlite_db.sql_database import Base
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
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

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    telegram_id: Column[INTEGER] = Column(INTEGER, nullable=False, unique=True)
    access_token: Column[VARCHAR] = Column(VARCHAR, nullable=False)

    @classmethod
    async def get_user_token(cls, telegram_id: int):
        """
        Метод выводящий токен пользователя.
        """

        token = await async_session.execute(
            select(cls).where(telegram_id == cls.telegram_id)
        )

        return token.scalar()
