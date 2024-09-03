"""Модуль таблицы 'users'"""

from api.database.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BYTEA, BOOLEAN, BIGINT


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

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    telegram_id: Column[BIGINT] = Column(BIGINT, nullable=False, unique=True)
    name: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    surname: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    is_active: Column[BOOLEAN] = Column(BOOLEAN, default=True)
    hashed_password: Column[BYTEA] = Column(BYTEA)

    habits = relationship("Habit", backref="habits")
