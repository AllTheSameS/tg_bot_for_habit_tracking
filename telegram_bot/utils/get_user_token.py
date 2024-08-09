import requests

from telegram_bot.sqlite_db.models.models import UserToken
from fastapi.exceptions import HTTPException
from fastapi import status
from settings import settings


async def get_token(telegram_id: int):

    token = await UserToken.get_user_token(telegram_id=telegram_id)

    if token:

        headers = {
            "Authorization": token.access_token,
        }

        response = requests.get(f"{settings.base_url}/user_info", headers=headers)

        if response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token error",
            )

        else:
            return token

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
