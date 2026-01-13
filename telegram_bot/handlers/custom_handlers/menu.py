from loader import bot
from telebot.types import CallbackQuery, Message, Any
from telegram_bot.utils.get_user_token import get_header
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from typing import Dict


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
async def menu(message: CallbackQuery | Message) -> None:
    """
    Главное меню.
    """
    context: Dict[str, Any] = extract_context(call_or_message=message)
    header: dict = await get_header(
        telegram_id=context['user_id'],
    )

    if header:
        await bot.edit_message_text(
            chat_id=context['chat_id'],
            message_id=context['message_id'],
            text="Главное меню.",
            reply_markup=inline_keyboard_manager.main_menu(),
        )
