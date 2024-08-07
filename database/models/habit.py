from database.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, DATE


class Habit(Base):
    __tablename__ = "habits"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(INTEGER, ForeignKey("users.id"), nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))
