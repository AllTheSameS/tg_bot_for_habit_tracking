from loader import bot
from telegram_bot import handlers
from telegram_bot.bot_default_command import set_default_commands
from telebot.asyncio_filters import StateFilter
from telegram_bot.sqlite_db.sql_database import engine, Base


import asyncio


async def start():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)

    await set_default_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(start())
