

async def cancel(bot, user_id: int, message_id: int, chat_id: int, keyboard):
    await bot.delete_state(
            user_id=user_id,
        )
    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id - 1,
    )
    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )
    await bot.send_message(
        chat_id=chat_id,
        text="Главное меню.",
        reply_markup=keyboard,
    )