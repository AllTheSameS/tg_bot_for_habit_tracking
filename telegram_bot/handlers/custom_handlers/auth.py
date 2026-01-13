"""
Модуль авторизации пользователя.

"""

from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot.states.states import UserLoginStates
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from telegram_bot.utils.insert_token_db import insert_token
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.handle_response import handle_error_api_response
from telegram_bot.managers.user_api_client import user_api_client
from telegram_bot.schemas.user_token_schema import UserTokenSchemas
from typing import Dict
from httpx import Response


@bot.callback_query_handler(func=lambda message: message.data == "login")
async def login_password(message: Message | CallbackQuery) -> None:
    """
    Обработчик кнопки 'Вход'.
    """
    context: Dict = extract_context(call_or_message=message)
    await bot.set_state(
        user_id=context['user_id'],
        state=UserLoginStates.login_password,
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data['main_message'] = context['message_id']
    await send_message(
        bot=bot,
        chat_id=context['chat_id'],
        message_id=context['message_id'],
        text="Введите пароль.",
        is_callback=context['is_callback'],
    )


@bot.message_handler(state=UserLoginStates.login_password)
async def login_user(message: Message | CallbackQuery) -> None:
    """
    Авторизация пользователя.
    """
    context: Dict = extract_context(call_or_message=message)
    data: dict = {
        "username": str(context['user_id']),
        "password": context['text'],
    }
    response_data: Response = await user_api_client.auth(
        data=data,
    )

    if response_data.status_code == 200:
        token = UserTokenSchemas(
            telegram_id=context['user_id'],
            access_token=f"{response_data.json()["token_type"]} {response_data.json()["access_token"]}",
        )
        await insert_token(
            token_info=token,
        )
        await send_message(
            bot=bot,
            chat_id=context['chat_id'],
            message_id=context['message_id'],
            text="Вы успешно вошли.\n" "Выберите действие.",
            reply_markup=inline_keyboard_manager.main_menu(),
            is_callback=context['is_callback']
        )
    elif  response_data.status_code == 404:
        await send_message(
            bot=bot,
            chat_id=context["chat_id"],
            message_id=context.get("message_id"),
            text="Привычка не найдена.",
            reply_markup=inline_keyboard_manager.registration(),
        )
    else:
        await handle_error_api_response(
            response=response_data,
            context=context
        )
    await bot.delete_message(
        chat_id=context['chat_id'],
        message_id=context['message_id'],
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        await bot.delete_message(
        chat_id=context['chat_id'],
        message_id=data['main_message'],
    )
    await bot.delete_state(
        user_id=context['user_id'],
        chat_id=context['chat_id'],
    )
