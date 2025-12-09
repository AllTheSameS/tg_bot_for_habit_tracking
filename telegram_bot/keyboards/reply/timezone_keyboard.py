from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def timezone() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(
            "📍 Отправить местоположение",
            request_location=True,
            ),
        KeyboardButton(
            "Пропустить",
        )
    )
    return markup
