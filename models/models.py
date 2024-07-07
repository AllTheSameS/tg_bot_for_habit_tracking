from database.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy import DATETIME


class User(Base):
    __tablename__ = "users"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    hashed_password: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    name: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    surname: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    role: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)

    habits = relationship("Habit", backref="habits")


class Habit(Base):
    __tablename__ = "habits"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    user_id: Column[INTEGER] = Column(INTEGER, ForeignKey="users.id", nullable=False)
    title: Column[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Column[VARCHAR] = Column(VARCHAR(300))
    amount_days: Column[INTEGER] = Column(INTEGER, default=21)
    start_date: Column[DATETIME] = Column(DATETIME)
