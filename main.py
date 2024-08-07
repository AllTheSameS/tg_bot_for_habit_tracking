from loader import bot
from telegram_bot import handlers
from telegram_bot.bot_default_command import set_default_commands
from telebot.asyncio_filters import StateFilter


import asyncio


async def start():
    await set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(start())
