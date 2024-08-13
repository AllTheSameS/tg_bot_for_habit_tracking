from sqlalchemy.orm import relationship

from api.database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER


class Habit(Base):
    __tablename__ = "habits"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))

    habits_tracking = relationship(
        "HabitTrackings",
        backref="habits_tracking",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
