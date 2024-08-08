from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Вывести информацию о себе", callback_data="Информация о пользователе"),
        InlineKeyboardButton(text="Создать привычку", callback_data="Создать привычку"),
    )
    return markup





