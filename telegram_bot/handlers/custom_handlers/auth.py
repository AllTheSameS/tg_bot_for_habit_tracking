"""Модуль авторизации пользователя."""

from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserLoginStates
from telegram_bot.keyboards.inline.main_keyboard import main_menu
from telegram_bot.keyboards.inline.start_keyboard import registration_kb
from telegram_bot.utils.insert_token_db import insert_token
from telegram_bot.schemas.user_token_schema import UserTokenSchemas
import httpx


@bot.callback_query_handler(func=lambda call: call.data == "login")
async def login_password(call: CallbackQuery) -> None:
    """
    Обработчик кнопки 'Вход'.
    """

    await bot.set_state(
        user_id=call.from_user.id,
        state=UserLoginStates.login_password,
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Введите пароль.",
        message_id=call.message.message_id,
    )


@bot.message_handler(state=UserLoginStates.login_password)
async def login_user(message: Message) -> None:
    """
    Авторизация пользователя.
    """

    data: dict = {
        "username": str(message.from_user.id),
        "password": message.text,
    }

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.base_url}/login", data=data
        )

    if response.status_code == 200:

        token = UserTokenSchemas(
            telegram_id=message.from_user.id,
            access_token=f"{response.json()["token_type"]} {response.json()["access_token"]}",
        )

        await insert_token(
            token_info=token,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text="Вы успешно вошли.\n" "Выберите действие.",
            reply_markup=main_menu(),
        )

    elif response.status_code == 401:

        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.id,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text="Введен неверный пароль.",
        )
        return

    elif response.status_code == 403:

        await bot.send_message(
            chat_id=message.chat.id,
            text="Пользователь заблокирован.",
        )

    elif response.status_code == 404:

        await bot.send_message(
            chat_id=message.chat.id,
            text="Вы не зарегистрированы.",
            reply_markup=registration_kb(),
        )

    elif response.status_code >= 500:

        await bot.send_message(
            chat_id=message.chat.id,
            text="Ошибка сервера.",
        )

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.id,
    )

    await bot.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
