"""Модуль таблицы 'users'"""

from api.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    """
    Таблица пользователей.
    Attributes:
        id: ID пользователя.
        telegram_id: Телеграм ID пользователя.
        name: Имя пользователя.
        surname: Фамилия пользователя.
        is_active: Активность пользователя.
        hashed_password: Пароль пользователя.
        habits: Связь с таблицей 'habits'.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[bytes]
    timezone: Mapped[str] = mapped_column(String(50), default='UTC')

    habits = relationship("Habit", backref="habits")
