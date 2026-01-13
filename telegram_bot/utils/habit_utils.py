from typing import Dict, Any
from loader import bot
from telegram_bot.managers.user_api_client import user_api_client
from telegram_bot.utils.get_user_token import get_header
from telegram_bot.utils.handle_response import handle_error_api_response
from telegram_bot.utils.format_habit_info import format_habit_info
from telegram_bot.utils.send_message import send_message


async def get_user_header(context: Dict[str, Any]) -> Dict[str, Any] | None:
    """Получение заголовка пользователя."""
    return await get_header(telegram_id=context['user_id'])


async def handle_api_error(response, context: Dict[str, Any]) -> None:
    """Обработка ошибок API."""
    if response.status_code >= 400:
        await handle_error_api_response(response=response, context=context)


async def get_user_timezone(header: Dict[str, Any]) -> str:
    """Получение часового пояса пользователя."""
    user_response = await user_api_client.get_user(headers=header)
    if user_response.status_code >= 400:
        return None
    return user_response.json().get('timezone', None)


async def format_and_send_habit_info(habit_data: Dict, user_timezone: str, context: Dict[str, Any], reply_markup=None, is_callback: bool = False) -> None:
    """Форматирование и отправка информации о привычке."""

    habit_info = format_habit_info(habit_data, user_timezone)
    await send_message(
        bot=bot,
        chat_id=context["chat_id"],
        message_id=context["message_id"],
        text=habit_info,
        reply_markup=reply_markup,
        is_callback=is_callback
    )
