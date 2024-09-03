from loader import bot
from telebot.types import CallbackQuery, Message
from telegram_bot.utils.get_user_token import get_header
from telegram_bot.keyboards.inline.main_keyboard import main_menu


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
async def menu(call: CallbackQuery) -> None:
    """
    Главное меню.
    """
    header: dict = await get_header(
        telegram_id=call.from_user.id,
    )

    if header:

        await bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            text="Главное меню.",
            reply_markup=main_menu(),
        )
