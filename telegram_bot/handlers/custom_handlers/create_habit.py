from typing import Any, Dict, List
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from httpx import Response

from telegram_bot.utils.handle_response import handle_error_api_response
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.format_title import format_title
from telegram_bot.utils.actual_location import actual_location
from telegram_bot.utils.cancel import cancel
from telegram_bot.utils.format_habit_info import format_habit_info
from telegram_bot.managers.user_api_client import user_api_client
from telegram_bot.managers.habit_api_client import habit_api_client
from telegram_bot.states.states import UserCreateHabitStates
from telegram_bot.keyboards.reply_keyboards import reply_keyboard_manager
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from telegram_bot.utils.get_user_token import get_header
from alerts.reminder_habits import reminder_habits
from alerts.main import scheduler
from loader import bot


@bot.message_handler(commands=["create_habit"])
@bot.callback_query_handler(func=lambda message: message.data == "create_habit")
async def create_habit_title(message: Message | CallbackQuery) -> None:
    """
    Процесс создание новой привычки.
    """
    context: Dict = extract_context(call_or_message=message)
    header: Dict = await get_header(context['user_id'])
    if header:
        await bot.set_state(
            user_id=context['user_id'],
            state=UserCreateHabitStates.habit_title,
        )

        async with bot.retrieve_data(user_id=context['user_id']) as data:
            data["header"] = header

        await bot.delete_message(
                chat_id=context['chat_id'],
                message_id=context['message_id'],
            )
        await bot.send_message(
            chat_id=context['chat_id'],
            text="Введите название привычки.",
            reply_markup=reply_keyboard_manager.cancel(),
        )
    else:
        return


@bot.message_handler(state=UserCreateHabitStates.habit_title)
async def create_habit_description(message: Message | CallbackQuery) -> None:
    """
    Процесс создание новой привычки.
    После ввода названия привычки.
    """
    context: Dict = extract_context(call_or_message=message)
    if context["text"] == 'Отмена':
        await cancel(
            bot=bot,
            user_id=context['user_id'],
            message_id=context['message_id'],
            chat_id=context['chat_id'],
            keyboard=inline_keyboard_manager.main_menu(),
            )
        return

    context['text'] = format_title(context['text'])
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["title"] = context['text']
    response_data: Response = await habit_api_client.get_all_habits(
        headers=data['header'],
    )
    titles: List = [habit['title'] for habit in response_data.json()]
    if context['text'] in titles:
        await bot.send_message(
            chat_id=context['chat_id'],
            text="Название уже существует.\nВведите другое название.",
        )
        return
    await bot.set_state(
        user_id=context['user_id'],
        state=UserCreateHabitStates.habit_description,
    )

    async with bot.retrieve_data(
        user_id=context['user_id'],
    ) as data:
        data["title"] = context['text']

    await bot.send_message(
        chat_id=context['chat_id'],
        text="Введите описание привычки.",
    )


@bot.message_handler(state=UserCreateHabitStates.habit_description)
async def create_habit_alert_time(message: Message | CallbackQuery) -> None:
    """
    Процесс создание новой привычки.
    После ввода описания привычки.
    """
    context: Dict = extract_context(call_or_message=message)
    if context["text"] == 'Отмена':
        await cancel(
            bot=bot,
            user_id=context['user_id'],
            message_id=context['message_id'],
            chat_id=context['chat_id'],
            keyboard=inline_keyboard_manager.main_menu(),
            )
        return
    await bot.set_state(
        user_id=context['user_id'],
        state=UserCreateHabitStates.habit_alert_time,
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["description"] = context['text']
        header: Any = data['header']

    response_data: Response = await user_api_client.get_user(
        headers=header,
    )
    response_data = response_data.json()
    if not response_data['timezone'] or response_data['timezone'] == 'UTC':
        await bot.send_message(
            chat_id=context['chat_id'],
            text="Ваша геолокация не определена.",
            reply_markup=reply_keyboard_manager.timezone(),
        )
    else:
        data['user_timezone'] = response_data['timezone']
        await bot.send_message(
            chat_id=context['chat_id'],
            text="Введите время оповещения привычки.",
            reply_markup=inline_keyboard_manager.skip(),
        )


@bot.message_handler(state=UserCreateHabitStates.habit_alert_time, content_types=['location'])
async def handle_actual_location(message: Message | CallbackQuery) -> None:
    context: Dict[str, Any] = extract_context(message)
    if message.location is None:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text="❌ Не удалось получить местоположение",
            is_callback=context["is_callback"],
        )
        return
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        latitude: float = message.location.latitude
        longitude: float = message.location.longitude
        location: str = await actual_location(
            latitude=latitude,
            longitude=longitude,
            header=data['header'],
        )
        data['user_timezone'] = location['timezone']
        await bot.delete_message(
            chat_id=context['chat_id'],
            message_id=context['message_id'],
        )
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text="✅ Часовой пояс установлен.\nВведите время оповещения привычки.",
            reply_markup=ReplyKeyboardRemove(),
            is_callback=context["is_callback"],
        )


@bot.callback_query_handler(func=lambda call: call.data == "skip")
@bot.message_handler(state=UserCreateHabitStates.habit_alert_time)
async def create_new_habit(message: Message | CallbackQuery) -> None:
    context: Dict[str, Any] = extract_context(call_or_message=message)
    alert_time: str = context['text']
    if context['text'] == 'Пропустить':
        alert_time: str = None

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data['alert_time'] = alert_time
        response_data: Response = await habit_api_client.create(
            data=data,
            headers=data["header"],
        )
        response_data = response_data.json()
    await bot.delete_state(
        user_id=context['user_id'],
    )
    if response_data:
        if alert_time is None:
            alert_time: str = 'Не назначено.'
        else:
            alert_time = response_data["habits_tracking"][0]["alert_time"]
            hour, minute = alert_time[:5].split(":")

            scheduler.add_job(
                id=str(response_data["id"]),
                func=reminder_habits,
                trigger="cron",
                hour=int(hour),
                minute=int(minute),
                args=(
                    context['user_id'],
                    response_data["title"],
                ),
            )
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text=(
                f"Привычка добавлена!\n\n{
                    format_habit_info(
                        habit_data=response_data,
                        user_timezone=data['user_timezone'],
                        )
                    }"
            ),
            reply_markup=inline_keyboard_manager.main_menu(),
            is_callback=context["is_callback"],
        )

    else:
        await handle_error_api_response(
            response=response_data,
            context=context,
        )
