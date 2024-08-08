from pydantic import BaseModel


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str
