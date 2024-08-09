from pydantic import BaseModel, ConfigDict


class HabitSchemas(BaseModel):
    model_config = ConfigDict()

    title: str
    description: str
    alert_time: str

