from api.database.database import Base
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, BYTEA, BOOLEAN


class User(Base):
    __tablename__ = "users"

    id: Column[INTEGER] = Column(INTEGER, primary_key=True)
    telegram_id: Column[INTEGER] = Column(INTEGER, nullable=False, unique=True)
    name: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    surname: Column[VARCHAR] = Column(VARCHAR(20), nullable=False)
    is_active: Column[BOOLEAN] = Column(BOOLEAN, default=True)
    hashed_password: Column[BYTEA] = Column(BYTEA)

    habits = relationship("Habit", backref="habits")
