from pydantic import BaseModel, ConfigDict, field_validator
from api.schemas.habit_tracking_schema import HabitTrackingSchema
from typing import List
import re


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
    timezone: str | None = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) > 50:
            raise ValueError('Title must be less than 50 characters')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if len(v) > 300:
            raise ValueError('Description must be less than 300 characters')
        return v.strip()

    @field_validator('alert_time')
    @classmethod
    def validate_alert_time(cls, v):
        if v is None:
            return v
        if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', v):
            raise ValueError('Alert time must be in HH:MM format')
        return v


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
