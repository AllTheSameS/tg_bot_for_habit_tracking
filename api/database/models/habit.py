"""Модуль таблицы 'habits'"""

from sqlalchemy.orm import relationship, Mapped
from api.database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER


class Habit(Base):
    """
    Таблица привычки.

    Attributes:
        id: ID привычки.
        user_id: ID пользователя.
        title: Название привычки.
        description: Описание привычки.
        habits_tracking: Связь с таблицей 'habit_trackings'.
    """

    __tablename__ = "habits"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))

    habits_tracking = relationship(
        "HabitTrackings",
        backref="habits_tracking",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
