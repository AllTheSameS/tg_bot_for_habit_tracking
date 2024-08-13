from pydantic import BaseModel


class NewHabitSchema(BaseModel):
    title: str
    description: str
