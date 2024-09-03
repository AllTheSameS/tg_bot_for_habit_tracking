from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def habits_kb(habits) -> InlineKeyboardMarkup:
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        *[
            InlineKeyboardButton(
                text=habit["title"], callback_data=f"title.{habit["title"]}"
            )
            for habit in habits
        ],
        InlineKeyboardButton(
            text="Назад",
            callback_data="main_menu",
        ),
    )

    return markup
