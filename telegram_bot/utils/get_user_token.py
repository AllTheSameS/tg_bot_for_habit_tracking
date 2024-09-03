import httpx
from loader import bot
from telegram_bot.sqlite_db.models.models import UserToken
from telegram_bot.keyboards.inline.start_keyboard import login_kb, registration_kb
from settings import settings
from typing import Any


async def get_header(telegram_id: int) -> dict:
    """
    Получение хедера.
    """

    token: Any = await UserToken.get_user_token(telegram_id=telegram_id)

    if token:

        header: dict = {
            "Authorization": token.access_token,
        }

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"{settings.base_url}/user_info", headers=header
            )

        if response.status_code == 401:
            await bot.send_message(
                chat_id=telegram_id,
                text="Войдите",
                reply_markup=login_kb(),
            )

        else:

            return header

    else:

        await bot.send_message(
            chat_id=telegram_id,
            text="Вы не зарегистрированы.",
            reply_markup=registration_kb(),
        )
