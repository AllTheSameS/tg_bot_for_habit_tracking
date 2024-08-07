from loader import bot, client
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserStates
import requests


@bot.message_handler(commands=["get_user_info"])
async def get_user_info(message: Message | CallbackQuery):

    async with bot.retrieve_data(message.from_user.id) as data:
        token = eval(data["token"].text)

    headers = {
        "Authorization": token["token"]
    }

    res = await client.get(f"{settings.base_url}/user_info", headers=headers)

    await bot.send_message(
        chat_id=message.from_user.id,
        text=res.text,
    )





