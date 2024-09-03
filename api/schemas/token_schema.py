from pydantic import BaseModel


class TokenSchemas(BaseModel):
    """
    Схема токена.
    Attributes:
        access_token: Токен.
        token_type: Тип токена.
    """

    access_token: str
    token_type: str
