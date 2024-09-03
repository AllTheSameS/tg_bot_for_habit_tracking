from loader import bot


async def reminder_habits(telegram_id: int, title: str) -> None:
    """
    Функция оповещения пользователей
    о выполнении личной привычки.
    """

    await bot.send_message(
        chat_id=telegram_id,
        text=f"Выполните привычку {title}.",
    )
