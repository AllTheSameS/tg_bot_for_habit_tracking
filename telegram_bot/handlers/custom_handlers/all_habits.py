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


@bot.message_handler(commands=["my_habits"])
@bot.callback_query_handler(func=lambda call: call.data == "all_habits")
async def get_all_habits(message: CallbackQuery | Message) -> None:
    """
    Обработчик кнопки 'Вывести все привычки'.
    """
    context: Dict[str, Any] = extract_context(message)
    header = await get_user_header(context)
    if not header:
        return
    response_data: Response = await habit_api_client.get_all_habits(headers=header)
    await handle_api_error(response_data, context)

    habits = response_data.json()
    if not habits:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text="У вас нет привычек.\nДобавьте новые привычки.",
            reply_markup=inline_keyboard_manager.create_habit(),
            is_callback=context["is_callback"]
        )
        return

    await bot.set_state(
        user_id=context['user_id'],
        state=AllHabitsStates.choice_habit,
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["header"] = header

    await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text="Выберите привычку.",
            reply_markup=inline_keyboard_manager.habits(habits),
            is_callback=context["is_callback"]
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("title."))
async def save_title_habit(message: CallbackQuery | Message) -> None:
    """Обработчик после выбора привычки."""
    context: Dict[str, Any] = extract_context(message)
    habit_title: str = message.data.split(".")[1]

    await bot.set_state(
        user_id=context["user_id"],
        state=AllHabitsStates.save_title_habit,
    )

    async with bot.retrieve_data(user_id=context["user_id"]) as data:
        response_data: Response = await habit_api_client.get_habit_by_title(
            title=habit_title,
            headers=data["header"],
        )
        await handle_api_error(response_data, context)

        habit_data = response_data.json()
        data['timezone'] = await get_user_timezone(data["header"])
        data['updated_habit_title'] = habit_data['title']
        await format_and_send_habit_info(
            habit_data, data['timezone'], context,
            reply_markup=inline_keyboard_manager.action(),
            is_callback=context["is_callback"]
        )
