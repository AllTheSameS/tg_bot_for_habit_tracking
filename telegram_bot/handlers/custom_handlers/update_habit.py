from loader import bot
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from telegram_bot.managers.habit_api_client import habit_api_client
from telegram_bot.managers.scheduler_manager import scheduler_manager
from telegram_bot.keyboards.reply_keyboards import reply_keyboard_manager
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from telegram_bot.utils.actual_location import actual_location
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.habit_utils import get_user_header, handle_api_error, get_user_timezone, format_habit_info
from telegram_bot.states.states import AllHabitsStates
from alerts.main import scheduler
from typing import Any, Dict
from httpx import Response
from telebot.types import InlineKeyboardMarkup


@bot.callback_query_handler(func=lambda call: call.data == "update")
async def action_update(message: CallbackQuery | Message) -> None:
    """
    Обработчик кнопки редактировать.
    Выводит что можно изменить.
    """
    context: Dict[str, Any] = extract_context(message)
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        await bot.set_state(
            user_id=context['user_id'],
            state=AllHabitsStates.action_update,
        )
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text="Выберите что изменить.",
            reply_markup=inline_keyboard_manager.update(data['updated_habit_title']),
            is_callback=context["is_callback"]
        )


@bot.message_handler(state=AllHabitsStates.update)
@bot.callback_query_handler(func=lambda call: call.data.startswith("data."))
async def new_data(message: CallbackQuery | Message) -> None:
    """
    Обработчик после выбора поля для изменения.
    """
    context: Dict[str, Any] = extract_context(message)
    fields: Dict[str, str] = {
        "title": "название",
        "description": "описание",
        "alert_time": "время напоминания",
    }

    await bot.set_state(
        user_id=context['user_id'],
        state=AllHabitsStates.new_data,
    )

    header = await get_user_header(context)
    if not header:
        return

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["field"] = message.data.split(".")[1]

    if data["field"] == "alert_time":
        if not data['timezone']:
            await bot.set_state(
                user_id=context['user_id'],
                state=AllHabitsStates.update_alert_time,
            )
            await bot.send_message(
                chat_id=context["chat_id"],
                text="Ваша геолокация не определена.",
                reply_markup=reply_keyboard_manager.timezone(),
            )
            return

        murkup: InlineKeyboardMarkup = inline_keyboard_manager.back_or_delete_alert_time("update")
    else:
        murkup: InlineKeyboardMarkup = inline_keyboard_manager.back("update")
    await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text=f"Введите новое {fields[data["field"]]}.",
            reply_markup=murkup,
            is_callback=context["is_callback"]
        )


@bot.message_handler(state=AllHabitsStates.update_alert_time, content_types=['location'])
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

    header = await get_user_header(context)
    if not header:
        return

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        latitude: float = message.location.latitude
        longitude: float = message.location.longitude
        location_message: str = await actual_location(
            latitude=latitude,
            longitude=longitude,
            header=header,
        )
        await bot.delete_message(
            chat_id=context['chat_id'],
            message_id=context['message_id'],
        )
        await bot.set_state(
            user_id=context['user_id'],
            state=AllHabitsStates.new_data,
        )
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text=location_message,
            reply_markup=ReplyKeyboardRemove(),
            is_callback=context["is_callback"],
        )


@bot.callback_query_handler(func=lambda call: call.data == "delete_alert_time")
@bot.message_handler(state=AllHabitsStates.new_data)
async def successful_update(message: Message | CallbackQuery) -> None:
    """
    Обработчик после ввода новых данных.
    Отправляет запрос на ресурс.
    """
    context: Dict[str, Any] = extract_context(message)

    header = await get_user_header(context)
    if not header:
        return

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        if data['field'] == 'alert_time' and context['text'] is None:
            context['text'] = None
        updated_data: Dict = {data['field']: context['text']}
        response_data: Response = await habit_api_client.update_habit(
            title=data['updated_habit_title'],
            data=updated_data,
            headers=header,
        )

        if response_data.status_code == 409:
            await send_message(
                bot=bot,
                chat_id=context["chat_id"],
                message_id=context.get("message_id"),
                text="Привычка с таким названием уже существует.\nВведите другое название.",
                is_callback=context.get("is_callback", False)
            )
            return
        await handle_api_error(response_data, context)

        habit_data = response_data.json()
        print(habit_data)
        if data['field'] == 'title':
            data['updated_habit_title'] = habit_data['title']
        if data["field"] == "alert_time" and context['text'] != 'Не установлено.':
            scheduler_manager.update_habit_job(
                job_id=habit_data["habits_tracking"][0]["habit_id"],
                title=habit_data['title'],
                alert_time=habit_data['habits_tracking'][0]['alert_time'],
                user_id=context['user_id'],
                scheduler=scheduler,
            )
        if data["field"] == "title":
            data['title'] = context['text']
        text: str = format_habit_info(
            habit_data=habit_data,
            user_timezone=data['timezone'],
            )
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context["message_id"],
            text=f"Привычка обновлена!\n\n{text}",
            reply_markup=inline_keyboard_manager.update(habit_data['title']),
            is_callback=context['is_callback'],
        )
