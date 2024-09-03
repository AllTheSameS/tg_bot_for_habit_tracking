from pydantic import BaseModel


class UserInfoSchema(BaseModel):
    """
    Схема пользователя.

    Attributes:
        name: Имя пользователя.
        surname: Фамилия пользователя.
        logged_in_at: Время входа.
    """

    name: str
    surname: str
    logged_in_at: int
