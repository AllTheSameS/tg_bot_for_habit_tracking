from loader import bot
from telebot.types import Message
from telegram_bot.states import states
from settings import settings
from telegram_bot.keyboards.inline.start_keyboards import registration_or_login
import requests


@bot.message_handler(commands=["start"])
async def cmd_start(message: Message):
    """Инициализация диалога с ботом"""

    welcome_text = (f"Привет, {message.chat.first_name}!\n"
                    f"Я чат-бот для трекинга привычек.\n ")

    await bot.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        reply_markup=registration_or_login(),
    )
