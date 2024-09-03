from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Создать привычку", callback_data="create_habit"),
        InlineKeyboardButton(text="Вывести все привычки", callback_data="all_habits"),
    )
    return markup


def create_habit_kb() -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Создать привычку", callback_data="create_habit"),
    )
    return markup
