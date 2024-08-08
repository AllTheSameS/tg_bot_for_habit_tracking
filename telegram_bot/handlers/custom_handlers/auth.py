"""Модуль авторизации пользователя."""
from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserStates
from telegram_bot.keyboards.inline.main_menu import main_menu
from telegram_bot.utils.insert_token_db import insert_token
from telegram_bot.schemas.user_token_schema import UserTokenSchemas
import requests


@bot.callback_query_handler(func=lambda call: call.data == "Вход")
async def login_user(call: CallbackQuery) -> None:
    await bot.set_state(
        user_id=call.from_user.id,
        state=UserStates.auth
    )

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Введите пароль",
    )


@bot.message_handler(state=UserStates.auth)
async def auth_user(message: Message) -> None:
    password = message.text

    data = {
        "username": str(message.from_user.id),
        "password": password,
    }

    response = requests.post(f"{settings.base_url}/login", data=data)

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserStates.main_menu,
    )

    token = UserTokenSchemas(
        telegram_id=message.from_user.id,
        access_token=f"{response.json()["token_type"]} {response.json()["access_token"]}",
    )

    await insert_token(token_info=token)

    text = ("Авторизация прошла успешно.\n"
            "Вы в главном меню.\n"
            "Выберите действие.")

    await bot.delete_message(message.chat.id, message.id)

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=main_menu(),
    )

