from pydantic import BaseModel
from datetime import date


class HabitEditingSchema(BaseModel):
    title: str
    title_field: str | date
    new_info: str





