from pydantic import BaseModel
from datetime import date


class HabitSchema(BaseModel):
    user_id: int
    title: str
    description: str
    amount_days: int
    start_date: date
