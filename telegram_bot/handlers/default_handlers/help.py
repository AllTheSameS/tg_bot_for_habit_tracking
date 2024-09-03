from telebot.types import Message
from settings import settings
from loader import bot


@bot.message_handler(commands=["help"])
async def bot_help(message: Message) -> None:
    """
    Функция, которая выводит все команды бота.
    """
    commands = [
        f"/{command} - {desk}" for command, desk in settings.bot.default_commands
    ]
    text = (
        "Я чат-бот для трекинга привычек.\n\n"
        "Вы можете:\n\n"
        "Создавать, просматривать, редактировать и удалять свои ежедневные привычки.\n"
        "Можете отмечать каждую привычку как выполненную.\n\n"
        "Я могу:\n\n"
        "Переносить невыполненные привычки на следующий день.\n"
        "Присылать уведомление для напоминания пользователям отмечать выполнение привычек.\n\n"
        "Доступные команды:\n\n"
    )
    await bot.reply_to(message, text + "\n".join(commands))
