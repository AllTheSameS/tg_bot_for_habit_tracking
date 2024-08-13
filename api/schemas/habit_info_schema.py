from pydantic import BaseModel
from datetime import time


class HabitInfoSchema(BaseModel):
    title: str
    description: str
    alert_time: str
    count: int | None = None
