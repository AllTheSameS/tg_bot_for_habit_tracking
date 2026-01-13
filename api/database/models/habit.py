"""Модуль таблицы 'habits'"""

from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.database.database import Base
from sqlalchemy import ForeignKey, String


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

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(300))

    habits_tracking = relationship(
        "HabitTrackings",
        backref="habits_tracking",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
