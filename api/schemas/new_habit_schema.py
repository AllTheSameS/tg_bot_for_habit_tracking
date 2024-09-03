from pydantic import BaseModel
from api.schemas.habit_tracking_schema import HabitTrackingSchema
from typing import List


class NewHabitSchemaIn(BaseModel):
    """
    Схема новой привычки на входе.
    Attributes:
        title: Название привычки.
        description: Описание привычки.
        alert_time: Время оповещения.
    """

    title: str
    description: str
    alert_time: str | None = None


class NewHabitSchemaOut(BaseModel):
    """
    Схема новой привычки на выходе.
    Attributes:
        id: ID привычки.
        title: Название привычки.
        description: Описание привычки.
        user_id: ID пользователя.
        habits_tracking: Схема HabitTracking.
    """

    id: int
    title: str
    description: str
    user_id: int
    habits_tracking: List[HabitTrackingSchema]
