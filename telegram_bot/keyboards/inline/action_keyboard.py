from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def action_kb() -> InlineKeyboardMarkup:
    """Добавления кнопок действий."""

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Редактировать", callback_data="update"),
        InlineKeyboardButton(text="Выполнить", callback_data="perform"),
        InlineKeyboardButton(text="Удалить", callback_data="delete"),
        InlineKeyboardButton(text="Назад", callback_data="all_habits"),
    )

    return markup
