from typing import Optional
from telebot.async_telebot import AsyncTeleBot

async def send_message(bot: AsyncTeleBot, chat_id: int, message_id: Optional[int], text: str, reply_markup=None, is_callback: bool = True) -> None:
    """Универсальная функция отправки сообщений."""
    if is_callback and message_id:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=text,
            message_id=message_id,
            reply_markup=reply_markup,
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
        )