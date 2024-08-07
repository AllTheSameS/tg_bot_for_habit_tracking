from telebot.asyncio_handler_backends import StatesGroup, State


class UserStates(StatesGroup):
    registration = State()
    auth = State()
    main_menu = State()
