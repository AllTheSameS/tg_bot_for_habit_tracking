from pydantic import BaseModel


class HabitUpdateSchema(BaseModel):
    """
    Схема редактирования привычки.
    Attributes:
        title: Название привычки.
        description: Описание привычки.
        alert_time: Время оповещения.
    """

    title: str | None = None
    description: str | None = None
    alert_time: str | None = None
