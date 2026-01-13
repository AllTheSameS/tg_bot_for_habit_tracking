from httpx import Response
from loader import bot
from telegram_bot.sqlite_db.models.models import UserToken
from telegram_bot.managers.user_api_client import user_api_client
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from typing import Any, Dict


async def get_header(telegram_id: int) -> Dict | None:
    """
    Получение хедера.
    """
    token: Any = await UserToken.get_user_token(telegram_id=telegram_id)
    if token:
        header: dict = {
            "Authorization": token.access_token,
        }
        response_data: Response = await user_api_client.get_user(
            headers=header,
        )
        if response_data.status_code == 401:
            await bot.send_message(
                chat_id=telegram_id,
                text="Войдите",
                reply_markup=inline_keyboard_manager.login(),
            )
        else:
            return header
    else:
        await bot.send_message(
            chat_id=telegram_id,
            text="Пользователь не зарегистрирован.",
            reply_markup=inline_keyboard_manager.registration(),
        )
