from telebot.types import Message, CallbackQuery
from typing import Dict, Any


def extract_context(call_or_message: CallbackQuery | Message) -> Dict[str, Any]:
    """Извлечение контекста из сообщения или callback."""
    if isinstance(call_or_message, Message):
        return {
            "user_id": call_or_message.from_user.id,
            "chat_id": call_or_message.chat.id,
            "message_id": call_or_message.message_id,
            "text": call_or_message.text,
            "is_callback": False
        }
    else:
        return {
            "user_id": call_or_message.from_user.id,
            "chat_id": call_or_message.message.chat.id,
            "message_id": call_or_message.message.message_id,
            "text": None,
            "is_callback": True
        }