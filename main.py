"""Модуль запуска бота."""
import os
import logging

from loader import bot
from telegram_bot import handlers
from telegram_bot.bot_default_command import set_default_commands
from telebot.asyncio_filters import StateFilter
from telegram_bot.sqlite_db.sql_database import engine, Base
from alerts.main import scheduler_start

import asyncio

logger = logging.getLogger('telegram_bot.main')


async def start():
    logger.info("Запуск Telegram бота")

    try:
        logger.info("Создание таблиц базы данных")
        async with engine.begin() as session:
            await session.run_sync(Base.metadata.create_all)
        logger.info("Таблицы базы данных созданы")

        logger.info("Запуск планировщика")
        await scheduler_start()
        logger.info("Планировщик запущен")

        logger.info("Установка команд бота")
        await set_default_commands(bot)
        bot.add_custom_filter(StateFilter(bot))
        logger.info("Команды бота установлены, начинаем polling")

        await bot.infinity_polling()

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    os.environ["TZ"] = "UTC"
    asyncio.run(start())
