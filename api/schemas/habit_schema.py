from pydantic import BaseModel
from typing import List
from api.schemas.habit_tracking_schema import HabitTrackingSchema


class HabitSchema(BaseModel):
    """
    Схема привычки.
    Attributes:
        id: ID привычки.
        user_id: ID пользователя.
        title: Название привычки.
        description: Описание привычки.
        habits_tracking: Схема HabitTracking.
    """

    id: int
    user_id: int
    title: str
    description: str
    habits_tracking: List[HabitTrackingSchema]
