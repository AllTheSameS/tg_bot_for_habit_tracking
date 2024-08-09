from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserCreateHabitStates
from telegram_bot.keyboards.inline.main_menu import main_menu
from telegram_bot.schemas.habit_schema import HabitSchemas
from telegram_bot.states.states import UserStates
from fastapi.exceptions import HTTPException
import requests

from telegram_bot.utils.get_user_token import get_token


@bot.callback_query_handler(func=lambda call: call.data == "Создать привычку")
@bot.message_handler(commands=["create_habit"])
async def create_habit_title(call: CallbackQuery):
    """Создание новой привычки."""

    try:

        token = await get_token(call.from_user.id)
        async with bot.retrieve_data(user_id=call.from_user.id) as data:
            data["token"] = token.access_token
            data["telegram_id"] = token.telegram_id

    except HTTPException:
        await bot.set_state(
            user_id=call.from_user.id,
            state=UserStates.login,
        )
        return

    await bot.set_state(
        user_id=call.from_user.id,
        state=UserCreateHabitStates.habit_title,
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text="Введите название привычки.",
    )


@bot.message_handler(state=UserCreateHabitStates.habit_title)
async def create_habit_description(message: Message):

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_description
    )

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["title"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Введите описание привычки.",
    )


@bot.message_handler(state=UserCreateHabitStates.habit_description)
async def create_habit_alert_time(message: Message):

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_alert_time
    )

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["description"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Введите время оповещения привычки.",
    )


@bot.message_handler(state=UserCreateHabitStates.habit_alert_time)
async def create_new_habit(message: Message):

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_alert_time
    )

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["alert_time"] = message.text,

        header = {
            "Authorization": data["token"]
        }

        requests.post(f"{settings.base_url}/habit/create", json=data, headers=header)

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Привычка успешно добавлена.",
        reply_markup=main_menu(),
    )
