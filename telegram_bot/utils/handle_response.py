from httpx import Response
from typing import Dict, Any, Optional
from telegram_bot.utils.send_message import send_message
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from loader import bot


async def handle_error_api_response(response: Response, context: Dict[str, Any]) -> Optional[Dict]:
    """Обработка стандартных ошибкок API."""

    if response.status_code == 400:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Ошибка ввода данных.\nВведите корректные данные.",
            is_callback=context.get("is_callback", False)
        )
    elif response.status_code == 401:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Пользователь не авторизован.",
            reply_markup=inline_keyboard_manager.registration_or_login(),
            is_callback=context.get("is_callback", False)
        )
    elif response.status_code == 403:
        await bot.send_message(
            chat_id=context["chat_id"],
            text="Пользователь заблокирован.",
        )
    elif response.status_code == 404:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Привычка не найдена.",
            reply_markup=inline_keyboard_manager.main_menu(),
            is_callback=context.get("is_callback", False)
        )
    elif response.status_code == 409:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Пользователь уже зарегестрирован.",
            reply_markup=inline_keyboard_manager.login(),
            is_callback=context.get("is_callback", False)
        )
    elif response.status_code >= 500:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Ошибка сервера.",
            is_callback=context.get("is_callback", False)
        )
    return None
