from loader import bot
from telebot.types import CallbackQuery, Message
from telegram_bot.managers.habit_api_client import habit_api_client
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.habit_utils import get_user_header, handle_api_error, format_and_send_habit_info, get_user_timezone
from telegram_bot.states.states import AllHabitsStates
from typing import Any, Dict
from httpx import Response


@bot.callback_query_handler(func=lambda call: call.data == "perform")
async def action_perform(message: CallbackQuery | Message) -> None:
    """
    Обработчик кнопки 'Выполнить'.
    """
    context: Dict[str, Any] = extract_context(message)

    await bot.set_state(
        user_id=context['user_id'],
        state=AllHabitsStates.action_perform,
    )

    header = await get_user_header(context)
    if not header:
        return

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        response_data: Response = await habit_api_client.perform_habit(
            title=data["updated_habit_title"],
            headers=header,
        )

        await handle_api_error(response_data, context)

        if response_data.status_code == 200:
            user_timezone = await get_user_timezone(header)
            habit_data = response_data.json()
            await format_and_send_habit_info(
                habit_data, user_timezone, context,
                reply_markup=inline_keyboard_manager.action(),
                is_callback=context["is_callback"]
            )
        elif response_data.status_code == 204:
            text: str = f'🎉 21 день! Привычка "{data["updated_habit_title"]}" теперь официально стала твоей второй натурой. Так держать!'
            await send_message(
                bot=bot,
                chat_id=context["chat_id"],
                message_id=context["message_id"],
                text=text,
                reply_markup=inline_keyboard_manager.main_menu(),
                is_callback=context["is_callback"]
            )
