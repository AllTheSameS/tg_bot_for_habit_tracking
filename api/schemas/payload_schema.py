from pydantic import BaseModel, ConfigDict
from api.schemas.habit_schema import HabitSchema
from typing import List


class PayloadSchema(BaseModel):
    """
    Схема новой привычки на входе.
    Attributes:
        title: Название привычки.
        description: Описание привычки.
        alert_time: Время оповещения.
    """

    user_id: int
    telegram_id: int
    name: str
    surname: str
    timezone: str
    habits: List[HabitSchema]

    model_config = ConfigDict(from_attributes=True)