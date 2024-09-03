from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def registration_or_login() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Вход", callback_data="login"),
        InlineKeyboardButton(text="Регистрация", callback_data="registration"),
    )
    return markup


def registration_kb() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Регистрация", callback_data="registration"),
    )

    return markup


def login_kb() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Вход", callback_data="login"),
    )

    return markup
