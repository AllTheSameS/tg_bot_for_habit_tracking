from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int
    name: str
    surname: str
    telegram_id: int
    is_active: bool
    hashed_password: str | bytes
