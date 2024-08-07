from loader import bot
from telebot.types import CallbackQuery
from telegram_bot.states.states import UserStates
from telegram_bot.handlers.custom_handlers.get_user_info import get_user_info


@bot.callback_query_handler(func=lambda call: call.data == "Информация о пользователе")
async def registration_handler(call: CallbackQuery) -> None:
    await get_user_info(call)






