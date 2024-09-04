import httpx

from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserCreateHabitStates
from telegram_bot.keyboards.inline.main_keyboard import main_menu
from telegram_bot.keyboards.inline.start_keyboard import registration_or_login
from telegram_bot.keyboards.inline.skip_keyboard import skip
from telegram_bot.utils.get_user_token import get_header
from alerts.reminder_habits import reminder_habits
from alerts.main import scheduler
from telegram_bot.utils.true_time import true_time
from typing import Any


@bot.callback_query_handler(func=lambda call: call.data == "create_habit")
async def create_habit_title(call: CallbackQuery):
    """Создание новой привычки."""

    header: dict = await get_header(call.from_user.id)

    if header:
        await bot.set_state(
            user_id=call.from_user.id,
            state=UserCreateHabitStates.habit_title,
        )

        async with bot.retrieve_data(
            user_id=call.from_user.id,
        ) as data:
            data["header"] = header

        await bot.send_message(
            chat_id=call.from_user.id,
            text="Введите название привычки.",
        )


@bot.message_handler(state=UserCreateHabitStates.habit_title)
async def create_habit_description(message: Message):

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_description,
    )

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["title"] = message.text

    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите описание привычки.",
    )


@bot.message_handler(state=UserCreateHabitStates.habit_description)
async def create_habit_alert_time(message: Message):

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_alert_time,
    )

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["description"] = message.text

    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите время оповещения привычки.",
        reply_markup=skip(),
    )


@bot.callback_query_handler(func=lambda call: call.data == "skip")
@bot.message_handler(state=UserCreateHabitStates.habit_alert_time)
async def create_new_habit(message: Message):

    if isinstance(message, CallbackQuery):
        alert_time: None = None

    else:
        alert_time: str = message.text

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["alert_time"]: Any = alert_time

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.base_url}/habit/create",
            json=data,
            headers=data["header"],
        )

    if response.status_code == 201:

        if data["alert_time"]:
            alert_time = await true_time(response.json()["habits_tracking"][0]["alert_time"])

            hour, minute = alert_time.split(":")

            scheduler.add_job(
                id=str(response.json()["id"]),
                func=reminder_habits,
                trigger="cron",
                hour=int(hour),
                minute=int(minute),
                args=(
                    message.from_user.id,
                    response.json()["title"],
                ),
            )

        await bot.send_message(
            chat_id=message.from_user.id,
            text=(
                f"Привычка добавлена!\n\n"
                f"Название: {response.json()["title"]}\n"
                f"Описание: {response.json()["description"]}\n"
                f"Время оповещения: {alert_time}\n"
                f"Осталось дней: {response.json()["habits_tracking"][0]["count"]}"
            ),
            reply_markup=main_menu(),
        )

    elif response.status_code == 400:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Введите корректное время оповещения. Например, 07:00",
        )
        return

    elif response.status_code == 401:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Пользователь не авторизован.",
            reply_markup=registration_or_login(),
        )

    elif response.status_code == 409:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Привычка с таким названием уже существует.",
            reply_markup=main_menu(),
        )

    elif response.status_code >= 500:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка сервера.",
        )

    await bot.delete_state(
        user_id=message.from_user.id,
    )
