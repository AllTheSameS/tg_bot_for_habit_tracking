from loader import bot
from telebot.types import CallbackQuery
from telegram_bot.states.states import UserStates


@bot.callback_query_handler(func=lambda call: call.data == "Вход")
async def registration_handler(call: CallbackQuery) -> None:

    await bot.set_state(
        user_id=call.from_user.id,
        state=UserStates.auth,
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text="Введите пароль",
    )

