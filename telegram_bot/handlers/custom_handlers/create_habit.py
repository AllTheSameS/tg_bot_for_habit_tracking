from loader import bot
from telebot.types import Message, CallbackQuery
from settings import settings
from telegram_bot.states.states import UserCreateHabitStates
from telegram_bot.keyboards.inline.main_menu import main_menu
import requests

from telegram_bot.utils.get_user_token import get_token


@bot.callback_query_handler(func=lambda call: call.data == "Создать привычку")
async def create_habit_title(call: CallbackQuery):

    text = "Введите название привычки."

    await bot.set_state(
        user_id=call.from_user.id,
        state=UserCreateHabitStates.habit_title
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text=text,
    )


@bot.message_handler(state=UserCreateHabitStates.habit_title)
async def create_habit_description(message: Message | CallbackQuery):
    text = "Введите описание привычки."

    await bot.set_state(message.from_user.id, UserCreateHabitStates.habit_description)

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["title"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
    )


@bot.message_handler(state=UserCreateHabitStates.habit_description)
async def create_habit_alert_time(message: Message | CallbackQuery):
    text = "Введите время оповещения привычки."

    await bot.set_state(message.from_user.id, UserCreateHabitStates.habit_alert_time)

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["description"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
    )


@bot.message_handler(state=UserCreateHabitStates.habit_alert_time)
async def create_habit(message: Message | CallbackQuery):
    text = "Привычка успешно добавлена."

    await bot.set_state(message.from_user.id, UserCreateHabitStates.habit_alert_time)

    async with bot.retrieve_data(user_id=message.from_user.id) as data:
        data["description"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        reply_markup=main_menu(),
    )
