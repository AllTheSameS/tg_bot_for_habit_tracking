from loader import bot
from telebot.types import CallbackQuery, Message
from telegram_bot.managers.habit_api_client import habit_api_client
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.habit_utils import get_user_header, handle_api_error
from telegram_bot.states.states import AllHabitsStates
from typing import Any, Dict
from httpx import Response


@bot.callback_query_handler(func=lambda call: call.data == "delete")
async def action_delete(message: CallbackQuery | Message) -> None:
    """
    Обработчик кнопки 'Удалить'.
    """
    context: Dict[str, Any] = extract_context(message)
    await bot.set_state(
        user_id=context['user_id'],
        state=AllHabitsStates.action_delete,
    )

    header = await get_user_header(context)

    if not header:
        return

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        response_data: Response = await habit_api_client.delete_habit(
            title=data["updated_habit_title"],
            headers=header,
        )
        await handle_api_error(response_data, context)

        await send_message(
                bot=bot,
                chat_id=context["chat_id"],
                message_id=context["message_id"],
                text=f"Привычка '{data["updated_habit_title"]}' удалена.",
                reply_markup=inline_keyboard_manager.main_menu(),
                is_callback=context["is_callback"]
        )
