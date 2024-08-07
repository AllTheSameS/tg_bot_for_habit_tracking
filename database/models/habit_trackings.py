from database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, DATE


class HabitTrackings(Base):
    __tablename__ = "habit_trackings"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    habit_id: Column[INTEGER] = Column(INTEGER, ForeignKey("habit.id"), nullable=False)
    alert_time: Column[DATE] = Column(DATE)
    count: Column[INTEGER] = Column(INTEGER, default=21)






