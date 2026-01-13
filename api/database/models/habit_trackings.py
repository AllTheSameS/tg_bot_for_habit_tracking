"""Модуль таблицы 'habit_trackings'"""

from api.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time
from typing import Optional


class HabitTrackings(Base):
    """
    Таблица отслеживания привычек.

    Attributes:
        id: ID трекинга.
        habit_id: ID привычки.
        alert_time: Время оповещения.
        count: Счетчик дней.
    """

    __tablename__ = "habit_trackings"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), index=True)
    alert_time: Mapped[Optional[time]] = mapped_column(index=True)
    count: Mapped[int] = mapped_column(default=21)
