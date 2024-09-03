from pydantic import BaseModel
from datetime import time


class HabitTrackingSchema(BaseModel):
    """
    Схема трекинга привычек.
    Attributes:
        id: ID трекинга привычки.
        habit_id: ID привычки.
        alert_time: Время оповещения.
        count: Счетчик дней.
    """

    id: int
    habit_id: int
    alert_time: time | None
    count: int
