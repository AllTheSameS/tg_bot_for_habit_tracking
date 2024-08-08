from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserStates
from telegram_bot.utils.get_user_token import get_token
import requests


@bot.callback_query_handler(func=lambda call: call.data == "Информация о пользователе")
async def get_user_info(call: CallbackQuery):

    token = await get_token(telegram_id=call.from_user.id)

    headers = {
        "Authorization": token.access_token,
    }

    res = requests.get(f"{settings.base_url}/user_info", headers=headers)

    text = f"Полное имя {res.json()["surname"]} {res.json()["name"]}"

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
    )
