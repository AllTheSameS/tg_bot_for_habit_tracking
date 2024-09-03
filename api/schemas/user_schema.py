from pydantic import BaseModel


class UserRegistrationSchema(BaseModel):
    """
    Схема регистрации пользователя.

    Attributes:
        name: Имя пользователя.
        surname: Фамилия пользователя.
        telegram_id: Телеграм ID пользователя.
        is_active: Активность пользователя.
        hashed_password: Пароль пользователя.
    """

    name: str
    surname: str
    telegram_id: int
    is_active: bool
    hashed_password: str | bytes


class UserLoginSchema(UserRegistrationSchema):
    """
    Схема пользователя при авторизации.
    """

    id: int
