from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def back(call_back) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=call_back),
    )
    return markup


def back_or_delete_alert_time(call_back) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Удалить", callback_data="delete_alert_time"),
        InlineKeyboardButton(text="Назад", callback_data=call_back),
    )
    return markup
