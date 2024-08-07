from telebot.types import BotCommand

from settings import settings


async def set_default_commands(bot):
    """
    Функция, которая добавляет команды боту.
    """

    await bot.set_my_commands([BotCommand(*i) for i in settings.bot.default_commands])





