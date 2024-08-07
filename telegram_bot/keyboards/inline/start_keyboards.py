from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def registration_or_login() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Вход", callback_data="Вход"),
        InlineKeyboardButton(text="Регистрация", callback_data="Регистрация"),
    )
    return markup
