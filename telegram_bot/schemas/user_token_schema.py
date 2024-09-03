from pydantic import BaseModel


class UserTokenSchemas(BaseModel):
    """
    Схема токена пользователя.

    Attributes:
        telegram_id: Телеграм ID.
        access_token: Токен.
    """

    telegram_id: int
    access_token: str
