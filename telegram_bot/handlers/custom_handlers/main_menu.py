from loader import bot
from telebot.types import Message
from telegram_bot.states.states import UserStates


@bot.message_handler(commands=["main_menu"], states=UserStates.main_menu)
async def main_menu(message: Message) -> None:
    """Главное меню"""

    await bot.send_message(
        chat_id=message.from_user.id,
        text="dawd",
    )





