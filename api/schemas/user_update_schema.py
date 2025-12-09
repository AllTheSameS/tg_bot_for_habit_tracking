from pydantic import BaseModel, field_validator
from api.auth.utils import hash_password


class UserUpdateSchemaIn(BaseModel):
    """
    Схема регистрации пользователя.

    Attributes:
        name: Имя пользователя.
        surname: Фамилия пользователя.
        timezone: Локация пользователя.
        hashed_password: Пароль пользователя.
    """

    name: str | None = None
    surname: str | None = None
    timezone: str | None = None
    hashed_password: str | None = None

    class Config:
        from_attributes = True

    @field_validator("hashed_password", mode="after")
    def hash_password(cls, value: str | None) -> bytes | None:
        if value is None:
            return value
        return hash_password(value)



class UserUpdateSchemaOut(UserUpdateSchemaIn):
    """
    Схема пользователя при авторизации.
    """
    id: int
