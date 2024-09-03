from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def update_kb(call_back) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Название", callback_data="data.title"),
        InlineKeyboardButton(text="Описание", callback_data="data.description"),
        InlineKeyboardButton(text="Время оповещения", callback_data="data.alert_time"),
        InlineKeyboardButton(text="Назад", callback_data=f"title.{call_back}"),
    )
    return markup
