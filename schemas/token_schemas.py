from pydantic import BaseModel


class TokenSchemas(BaseModel):
    token: str
