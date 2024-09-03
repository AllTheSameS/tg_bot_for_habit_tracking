from loader import bot
from api.database.database import async_session
from api.database.models.user import User
from sqlalchemy import select
from typing import Any


async def reminder() -> None:
    """
    Функция оповещения пользователей о выполнении привычек.
    """

    async with async_session as session:
        all_telegram_id: Any = await session.execute(
            select(
                User.telegram_id,
            )
        )

        for telegram_id in all_telegram_id.scalars().all():

            await bot.send_message(
                chat_id=telegram_id, text="Не забудьте сегодня выполнить свои привычки."
            )
