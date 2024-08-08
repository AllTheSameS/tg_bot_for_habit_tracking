from telebot.asyncio_handler_backends import StatesGroup, State


class UserStates(StatesGroup):
    registration = State()
    auth = State()
    main_menu = State()


class UserCreateHabitStates(StatesGroup):
    habit_title = State()
    habit_description = State()
    habit_alert_time = State()
