from telegram_bot.schemas.user_token_schema import UserTokenSchemas
from telegram_bot.sqlite_db.models.models import UserToken


async def get_token(telegram_id: int):
    token = await UserToken.get_user_token(telegram_id=telegram_id)
    return token
