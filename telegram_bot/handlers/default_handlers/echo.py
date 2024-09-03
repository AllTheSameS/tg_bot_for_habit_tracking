from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: True)
async def bot_echo(message: Message) -> None:
    """
    Функция, которая ловит неизвестные команды.
    """
    await bot.reply_to(
        message,
        f"Неизвестная команда.\n" f"Введите команду /help.",
    )
