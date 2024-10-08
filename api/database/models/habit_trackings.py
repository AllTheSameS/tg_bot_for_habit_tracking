"""Модуль таблицы 'habit_trackings'"""

from api.database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TIME


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

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    habit_id: Column[INTEGER] = Column(
        INTEGER, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False
    )
    alert_time: Column[TIME] = Column(TIME())
    count: Column[INTEGER] = Column(INTEGER, default=21)
