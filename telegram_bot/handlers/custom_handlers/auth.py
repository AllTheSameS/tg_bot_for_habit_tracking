from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserStates
from telegram_bot.keyboards.inline.main_menu import main_menu
import requests


@bot.message_handler(commands=["authorisation"])
async def login_user(message: Message | CallbackQuery) -> None:
    await bot.set_state(
        user_id=message.from_user.id,
        state=UserStates.auth
    )

    await bot.send_message(
        chat_id=message.from_user.id,
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

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["token"] = response

    text = ("Авторизация прошла успешно.\n"
            "Вы в главном меню.\n"
            "Выберите действие.")

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=main_menu(),
    )





