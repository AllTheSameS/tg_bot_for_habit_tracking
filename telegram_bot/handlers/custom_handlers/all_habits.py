from loader import bot
from telebot.types import CallbackQuery, Message
from settings import settings
from telegram_bot.utils.get_user_token import get_header
from telegram_bot.utils.true_time import true_time
from telegram_bot.keyboards.inline.habits_keyboard import habits_kb
from telegram_bot.keyboards.inline.action_keyboard import action_kb
from telegram_bot.keyboards.inline.main_keyboard import main_menu, create_habit_kb
from telegram_bot.keyboards.inline.update_data_keyboard import update_kb
from telegram_bot.keyboards.inline.start_keyboard import registration_or_login
from telegram_bot.keyboards.inline.back_keyboard import back, back_or_delete_alert_time
from telegram_bot.states.states import AllHabitsStates
from alerts.reminder_habits import reminder_habits
from alerts.main import scheduler
from typing import Any
from apscheduler.job import Job

import httpx


@bot.callback_query_handler(func=lambda call: call.data == "all_habits")
async def get_all_habits(call: CallbackQuery) -> None:
    """

    Обработчик кнопки 'Вывести все привычки'.

    """

    header: dict = await get_header(
        telegram_id=call.from_user.id,
    )

    if header:

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"{settings.base_url}/habit/all", headers=header
            )

        if response.json():

            if response.status_code == 200:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Выберите привычку.",
                    message_id=call.message.message_id,
                    reply_markup=habits_kb(response.json()),
                )

                await bot.set_state(
                    user_id=call.from_user.id,
                    state=AllHabitsStates.choice_habit,
                )

                async with bot.retrieve_data(user_id=call.from_user.id) as data:
                    data["headers"] = header

            elif response.status_code == 401:

                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Пользователь не авторизован.",
                )

        else:

            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                text="У вас нет привычек.\n" "Добавьте новые привычки.",
                message_id=call.message.message_id,
                reply_markup=create_habit_kb(),
            )


@bot.callback_query_handler(func=lambda call: call.data.startswith("title."))
async def save_title_habit(call: CallbackQuery) -> None:
    """
    Обработчик после выбора привычки.
    """

    await bot.set_state(
        user_id=call.from_user.id,
        state=AllHabitsStates.save_title_habit,
    )

    async with bot.retrieve_data(user_id=call.from_user.id) as data:
        data["habit"] = call.data.split(".")[1]

        async with httpx.AsyncClient() as client:

            response: httpx.Response = await client.get(
                f"{settings.base_url}/habit/title/{data["habit"]}",
                headers=data["headers"],
            )

            if response.status_code == 200:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text=(
                        f"Название: {response.json()["title"]}\n"
                        f"Описание: {response.json()["description"]}\n"
                        f"Время оповещения: {await true_time(response.json()["habits_tracking"][0]["alert_time"])}\n"
                        f"Осталось дней: {response.json()["habits_tracking"][0]["count"]}"
                    ),
                    message_id=call.message.message_id,
                    reply_markup=action_kb(),
                )

            elif response.status_code == 401:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Пользователь не авторизован.",
                    message_id=call.message.message_id,
                    reply_markup=registration_or_login(),
                )

            elif response.status_code == 404:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Привычка не найдена.",
                    message_id=call.message.message_id,
                    reply_markup=main_menu(),
                )

            elif response.status_code >= 500:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Ошибка сервера.",
                    message_id=call.message.message_id,
                )


@bot.callback_query_handler(func=lambda call: call.data == "perform")
async def action_perform(call: CallbackQuery) -> None:
    """
    Обработчик кнопки 'Выполнить'.
    """

    await bot.set_state(
        user_id=call.from_user.id,
        state=AllHabitsStates.action_perform,
    )

    async with bot.retrieve_data(user_id=call.from_user.id) as data:

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.patch(
                f"{settings.base_url}/habit/perform/{data["habit"]}",
                headers=data["headers"],
            )

            if response.status_code == 200:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text=(
                        f"Привычка выполнена!\n\n"
                        f"Название: {response.json()["title"]}\n"
                        f"Описание: {response.json()["description"]}\n"
                        f"Время оповещения: {await true_time(response.json()["habits_tracking"][0]["alert_time"])}\n"
                        f"Осталось дней: {response.json()["habits_tracking"][0]["count"]}"
                    ),
                    message_id=call.message.message_id,
                    reply_markup=action_kb(),
                )

            if response.status_code == 204:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text=f"Привычка '{data["habit"]}' выполнена!",
                    message_id=call.message.message_id,
                    reply_markup=main_menu(),
                )

            elif response.status_code == 401:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Пользователь не авторизован.",
                    message_id=call.message.message_id,
                    reply_markup=registration_or_login(),
                )

            elif response.status_code == 404:
                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Привычка не найдена.",
                    message_id=call.message.message_id,
                    reply_markup=main_menu(),
                )

            elif response.status_code >= 500:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Ошибка сервера.",
                    message_id=call.message.message_id,
                )


@bot.callback_query_handler(func=lambda call: call.data == "delete")
async def action_delete(call: CallbackQuery) -> None:
    """
    Обработчик кнопки 'Удалить'.
    """

    await bot.set_state(
        user_id=call.from_user.id,
        state=AllHabitsStates.action_delete,
    )

    async with bot.retrieve_data(user_id=call.from_user.id) as data:

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.delete(
                f"{settings.base_url}/habit/remove/{data["habit"]}",
                headers=data["headers"],
            )

            if response.status_code == 204:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text=f"Привычка '{data["habit"]}' удалена.",
                    message_id=call.message.message_id,
                    reply_markup=main_menu(),
                )

            elif response.status_code == 401:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Пользователь не авторизован.",
                    message_id=call.message.message_id,
                    reply_markup=registration_or_login(),
                )

            elif response.status_code == 404:

                await bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    text="Привычка не найдена.",
                    message_id=call.message.message_id,
                    reply_markup=main_menu(),
                )

            elif response.status_code >= 500:

                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Ошибка сервера.",
                )


@bot.callback_query_handler(func=lambda call: call.data == "update")
async def action_update(call: CallbackQuery) -> None:
    """
    Обработчик кнопки редактировать.
    Выводит что можно изменить.
    """
    async with bot.retrieve_data(user_id=call.from_user.id) as data:

        await bot.set_state(
            user_id=call.from_user.id,
            state=AllHabitsStates.action_update,
        )
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="Выберите что изменить.",
            message_id=call.message.message_id,
            reply_markup=update_kb(data["habit"]),
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("data."))
async def new_data(call: CallbackQuery) -> None:
    """
    Обработчик после выбора поля для изменения.
    """

    fields = {
        "title": "название",
        "description": "описание",
        "alert_time": "временя напоминания",
    }

    await bot.set_state(
        user_id=call.from_user.id,
        state=AllHabitsStates.new_data,
    )

    async with bot.retrieve_data(user_id=call.from_user.id) as data:
        data["field"] = call.data.split(".")[1]

    if data["field"] == "alert_time":
        murkup = back_or_delete_alert_time("update")

    else:
        murkup = back("update")

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Введите новое {fields[data["field"]]}.",
        reply_markup=murkup,
    )


@bot.callback_query_handler(func=lambda call: call.data == "delete_alert_time")
@bot.message_handler(state=AllHabitsStates.new_data)
async def successful_update(message: Message) -> None:
    """
    Обработчик после ввода новых данных.
    Отправляет запрос на ресурс.
    """

    async with bot.retrieve_data(user_id=message.from_user.id) as data:

        if isinstance(message, CallbackQuery):
            message.text = None

        new_info: dict = {
            data["field"]: message.text,
        }

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.patch(
                f"{settings.base_url}/habit/update/{data["habit"]}",
                json=new_info,
                headers=data["headers"],
            )

        if data["field"] == "alert_time" and response.status_code == 200:

            alert_time: Any = await true_time(response.json()["habits_tracking"][0]["alert_time"])

            check_job: Job = scheduler.get_job(
                job_id=str(response.json()["habits_tracking"][0]["habit_id"]),
            )

            if alert_time:

                hour, minute = alert_time.split(":")

                if check_job:
                    check_job.reschedule(
                        trigger="cron",
                        hour=hour,
                        minute=minute,
                        timezone="Asia/Novosibirsk",
                    )

                else:
                    scheduler.add_job(
                        id=str(response.json()["id"]),
                        func=reminder_habits,
                        trigger="cron",
                        hour=int(hour),
                        minute=int(minute),
                        timezone="Asia/Novosibirsk",
                        args=(
                            message.from_user.id,
                            response.json()["title"],
                        ),
                    )
            else:

                if check_job:
                    check_job.remove()

        if response.status_code == 200:

            if data["field"] == "title":
                data["habit"] = message.text

            alert_time = await true_time(response.json()["habits_tracking"][0]["alert_time"])

            await bot.send_message(
                chat_id=message.from_user.id,
                text=(
                    f"Привычка успешно изменена!\n\n"
                    f"Название: {response.json()["title"]}\n"
                    f"Описание: {response.json()["description"]}\n"
                    f"Время оповещения: {alert_time}\n"
                    f"Осталось дней: {response.json()["habits_tracking"][0]["count"]}"
                ),
                reply_markup=update_kb(data["habit"]),
            )

        elif response.status_code == 400:

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Введите корректное время. Например 07:20",
            )
            return

        elif response.status_code == 401:

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Пользователь не авторизован.",
                reply_markup=registration_or_login(),
            )

        elif response.status_code == 404:

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Привычка не найдена.",
                reply_markup=main_menu(),
            )

        elif response.status_code == 409:

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Привычка с таким названием уже существует.",
            )
            return

        elif response.status_code >= 500:

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Ошибка сервера.",
            )
