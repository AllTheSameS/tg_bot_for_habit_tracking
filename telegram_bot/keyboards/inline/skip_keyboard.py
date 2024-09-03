from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def skip() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Пропустить", callback_data="skip"),
    )
    return markup
