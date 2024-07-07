from database import Base
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, INTEGER, BOOLEAN, TIMESTAMP


class User(Base):
    __talename__ = "users"

    id: Mapped[INTEGER] = Column(INTEGER, primary_key=True)
    name: Mapped[VARCHAR] = Column(VARCHAR(20), nullable=False)
    surname: Mapped[VARCHAR] = Column(VARCHAR(20), nullable=False)
    role: Mapped[VARCHAR] = Column(VARCHAR(20), nullable=False)
    habit: Mapped[ARRAY] = Column(ARRAY)


class Habit(Base):
    id: Mapped[INTEGER] = Column(INTEGER, primary_key=True)
    title: Mapped[VARCHAR] = Column(VARCHAR(50), nullable=False)
    description: Mapped[VARCHAR] = Column(VARCHAR(300))
    amount_days: Mapped[INTEGER] = Column(INTEGER, default=21)
    done: Mapped[BOOLEAN] = Column(BOOLEAN)
    start_date: Mapped[TIMESTAMP] = Column(TIMESTAMP)
