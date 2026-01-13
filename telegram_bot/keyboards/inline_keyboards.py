from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardManager:

    @staticmethod
    def action() -> InlineKeyboardMarkup:
        """Добавления кнопок действий."""

        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Редактировать", callback_data="update"),
            InlineKeyboardButton(text="Выполнить", callback_data="perform"),
            InlineKeyboardButton(text="Удалить", callback_data="delete"),
            InlineKeyboardButton(text="Назад", callback_data="all_habits"),
        )
        return markup

    @staticmethod
    def back(call_back) -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Назад", callback_data=call_back),
        )
        return markup

    @staticmethod
    def back_or_delete_alert_time(call_back) -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Удалить", callback_data="delete_alert_time"),
            InlineKeyboardButton(text="Назад", callback_data=call_back),
        )
        return markup

    @staticmethod
    def habits(habits) -> InlineKeyboardMarkup:
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

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Создать привычку", callback_data="create_habit"),
            InlineKeyboardButton(text="Вывести все привычки", callback_data="all_habits"),
        )
        return markup

    @staticmethod
    def create_habit() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Создать привычку", callback_data="create_habit"),
        )
        return markup

    @staticmethod
    def skip() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Пропустить", callback_data="skip"),
        )
        return markup

    @staticmethod
    def registration_or_login() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Вход", callback_data="login"),
            InlineKeyboardButton(text="Регистрация", callback_data="registration"),
        )
        return markup

    @staticmethod
    def registration() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Регистрация", callback_data="registration"),
        )

        return markup

    @staticmethod
    def login() -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Вход", callback_data="login"),
        )

        return markup

    @staticmethod
    def update(call_back) -> InlineKeyboardMarkup:
        markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="Название", callback_data="data.title"),
            InlineKeyboardButton(text="Описание", callback_data="data.description"),
            InlineKeyboardButton(text="Время оповещения", callback_data="data.alert_time"),
            InlineKeyboardButton(text="Назад", callback_data=f"title.{call_back}"),
        )
        return markup


inline_keyboard_manager: InlineKeyboardManager = InlineKeyboardManager()