from pydantic import BaseModel


class TokenSchemas(BaseModel):
    """
    Схема токена.
    Attributes:
        access_token: Токен.
        refresh_token: Refresh токен.
        token_type: Тип токена.
    """

    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    """
    Схема для refresh токена.
    Attributes:
        refresh_token: Refresh токен.
    """

    refresh_token: str
