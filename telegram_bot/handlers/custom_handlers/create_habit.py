from typing import Any
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
import httpx

from timezonefinder import TimezoneFinder
from settings import settings
from telegram_bot.states.states import UserCreateHabitStates
from telegram_bot.keyboards.inline.main_keyboard import main_menu
from telegram_bot.keyboards.inline.start_keyboard import registration_or_login
from telegram_bot.keyboards.inline.skip_keyboard import skip
from telegram_bot.keyboards.reply.timezone_keyboard import timezone
from telegram_bot.utils.get_user_token import get_header
from alerts.reminder_habits import reminder_habits
from alerts.main import scheduler
from loader import bot


@bot.message_handler(commands=["create_habit"])
@bot.callback_query_handler(func=lambda call: call.data == "create_habit")
async def create_habit_title(call: CallbackQuery) -> None:
    """
    Процесс создание новой привычки.
    """
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
    """
    Процесс создание новой привычки.
    После ввода названия привычки.
    """
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
async def create_habit_alert_time(message: Message) -> None:
    """
    Процесс создание новой привычки.
    После ввода описания привычки.
    """
    await bot.set_state(
        user_id=message.from_user.id,
        state=UserCreateHabitStates.habit_alert_time,
    )
    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["description"] = message.text
        header: Any = data['header']
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(
            f"{settings.base_url}/user_info", headers=header
        )
    if not response.json()['timezone'] or response.json()['timezone'] == 'UTC':
        await bot.send_message(
            chat_id=message.chat.id,
            text="Ваша геолокация не определена.",
            reply_markup=timezone(),
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введите время оповещения привычки.",
            reply_markup=skip(),
        )


@bot.message_handler(state=UserCreateHabitStates.habit_alert_time, content_types=['location'])
async def handle_actual_location(message: Message) -> None:
    if message.location is None:
        await bot.send_message(message.chat.id, "❌ Не удалось получить местоположение")
        return

    latitude: float = message.location.latitude
    longitude: float = message.location.longitude

    try:
        tf = TimezoneFinder()
        user_timezone: str | None = tf.timezone_at(lat=latitude, lng=longitude)

        if user_timezone:
            async with bot.retrieve_data(user_id=message.from_user.id) as data:
                data['timezone'] = user_timezone
                header: Any = data['header']
            async with httpx.AsyncClient() as client:
                response: httpx.Response = await client.patch(
                    f"{settings.base_url}/me",
                    headers=header,
                    json={"timezone": str(user_timezone)},
                )
            if response.status_code == 200:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.id,
                )
                await bot.send_message(
                    message.chat.id,
                    "✅ Часовой пояс установлен.\nВведите время оповещения привычки.",
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    "Ошибка установки часового пояса.\nПовторите попытку позже.",
                    reply_markup=ReplyKeyboardRemove(),
                )
        else:
            await bot.send_message(
                message.chat.id,
                "❌ Не удалось определить часовой пояс по координатам",
                )

    except Exception:
        await bot.send_message(message.chat.id, "❌ Произошла ошибка при определении часового пояса")


@bot.callback_query_handler(func=lambda call: call.data == "skip")
@bot.message_handler(state=UserCreateHabitStates.habit_alert_time)
async def create_new_habit(message: Message) -> None:
    if isinstance(message, CallbackQuery) or message.text == 'Пропустить':
        alert_time: None = None
    else:
        alert_time: str = message.text

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["alert_time"] = alert_time

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.base_url}/habit/create",
            json=data,
            headers=data["header"],
        )

    await bot.delete_state(
        user_id=message.from_user.id,
    )

    if response.status_code == 201:
        if data["alert_time"]:
            alert_time = response.json()["habits_tracking"][0]["alert_time"]

            hour, minute, _ = alert_time.split(":")

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

        alert_time = 'Не назначено.'

        if data["alert_time"]:
            alert_time = data["alert_time"]

        await bot.send_message(
            chat_id=message.from_user.id,
            text=(
                f"Привычка добавлена!\n\n"
                f"Название: {response.json()["title"]}\n"
                f"Описание: {response.json()["description"]}\n"
                f"Время оповещения: {data["alert_time"]}\n"
                f"Осталось дней: {response.json()["habits_tracking"][0]["count"]}"
            ),
            reply_markup=main_menu(),
        )

    elif response.status_code == 400:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Введите корректное время оповещения. Например, 07:00.\nЛибо попробуйте установить локацию заново.",
        )
        return

    elif response.status_code == 401:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Пользователь не авторизован.",
            reply_markup=registration_or_login(),
        )
        return

    elif response.status_code == 409:

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Привычка с таким названием уже существует.",
            reply_markup=main_menu(),
        )
        return

    elif response.status_code >= 500:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка сервера.",
        )
        return
