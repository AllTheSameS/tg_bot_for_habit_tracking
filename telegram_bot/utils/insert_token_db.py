from telegram_bot.schemas.user_token_schema import UserTokenSchemas
from telegram_bot.sqlite_db.sql_database import async_session
from telegram_bot.sqlite_db.models.models import UserToken
from typing import Any


async def insert_token(token_info: UserTokenSchemas) -> None:
    """Добавление токена в базу данных."""
    token: Any = await UserToken.get_user_token(telegram_id=token_info.telegram_id)

    if token is None:
        new_token: UserToken = UserToken(
            telegram_id=token_info.telegram_id,
            access_token=token_info.access_token,
        )
        async_session.add(new_token)
