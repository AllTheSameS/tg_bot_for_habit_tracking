from pydantic import BaseModel, ConfigDict, field_serializer
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

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('alert_time')
    def serialize_alert_time(self, time: time) -> str | None:
        return time.isoformat() if time else None
