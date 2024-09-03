"""Модуль стейтов."""

from telebot.asyncio_handler_backends import StatesGroup, State


class UserRegistrationStates(StatesGroup):
    """Стейты при регистрации пользователя."""

    registration_name = State()
    registration_surname = State()
    registration_password = State()


class UserLoginStates(StatesGroup):
    """Стейты при авторизации пользователя."""

    login = State()
    login_password = State()
    login_user = State()


class AllHabitsStates(StatesGroup):
    """Стейты работы с привычками."""

    choice_habit = State()
    save_title_habit = State()
    action_perform = State()
    action_delete = State()
    action_update = State()
    new_data = State()
    update = State()


class UserCreateHabitStates(StatesGroup):
    """Стейты при создании привычки."""

    habit_title = State()
    habit_description = State()
    habit_alert_time = State()
