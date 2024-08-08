from pydantic import BaseModel


class UserTokenSchemas(BaseModel):
    telegram_id: int
    access_token: str
