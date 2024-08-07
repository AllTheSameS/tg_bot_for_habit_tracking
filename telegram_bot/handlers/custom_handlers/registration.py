from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot.states import states
from settings import settings
from telegram_bot.states.states import UserStates
import requests


@bot.message_handler(commands=["registration"])
async def cmd_registration(message: Message | CallbackQuery) -> None:
    """Регистрация"""
    text = "Введите имя, фамилию и пароль."

    await bot.set_state(
        user_id=message.from_user.id,
        state=states.UserStates.registration,
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
    )


@bot.message_handler(state=states.UserStates.registration)
async def registration_user(message: Message) -> None:
    name, surname, password = message.text.split()

    data = {
        "name": name,
        "surname": surname,
        "telegram_id": message.from_user.id,
        "is_active": True,
        "hashed_password": password,
    }

    response = requests.post(f"{settings.base_url}/registration", json=data)

    text = (f"{response.json()["surname"]} {response.json()["name"]} успешно зарегистрирован.\n"
            f"Для входа введи пароль.")

    await bot.set_state(
        user_id=message.from_user.id,
        state=UserStates.auth,
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
    )
