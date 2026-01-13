from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class ReplyKeyboardManager:

    @staticmethod
    def cancel() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            KeyboardButton(
                "Отмена",
        ))
        return markup

    @staticmethod
    def timezone() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(
            KeyboardButton(
                "📍 Отправить местоположение",
                request_location=True,
                ),
            KeyboardButton(
                "Пропустить",
            ),
        )
        return markup


reply_keyboard_manager: ReplyKeyboardManager = ReplyKeyboardManager()