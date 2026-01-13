from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot.states import states
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.handle_response import handle_error_api_response
from telegram_bot.managers.user_api_client import user_api_client
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from typing import Any, Dict
from httpx import Response


@bot.callback_query_handler(func=lambda call: call.data == "registration")
async def cmd_registration(message: CallbackQuery | Message) -> None:
    """
    Процесс регистрации.
    После нажатия кнопки "Регистрация"
    """
    context: Dict[str, Any] = extract_context(call_or_message=message)

    await bot.set_state(
        user_id=context['user_id'],
        state=states.UserRegistrationStates.registration_name,
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["main_message_id"] = context['message_id']
    await send_message(
        bot=bot,
        chat_id=context["chat_id"],
        message_id=context["message_id"],
        text="Введите ваше имя.",
        reply_markup=None,
        is_callback=context["is_callback"],
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_name)
async def password_registration(message: CallbackQuery | Message) -> None:
    """
    Процесс регистрации.
    После ввода имени пользователя.
    """
    context: Dict[str, Any] = extract_context(call_or_message=message)
    await bot.set_state(
        user_id=context['user_id'],
        state=states.UserRegistrationStates.registration_surname,
    )

    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["name"] = context['text']
        main_message_id = data["main_message_id"]

    await bot.delete_message(
        chat_id=context['chat_id'],
        message_id=context['message_id'],
    )
    await send_message(
        bot=bot,
        chat_id=context["chat_id"],
        message_id=main_message_id,
        text="Введите вашу фамилию.",
        reply_markup=None,
        is_callback=True,
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_surname)
async def password_registration(message: CallbackQuery | Message) -> None:
    """
    Процесс регистрации.
    После ввода фамилии пользователя.
    """
    context: Dict[str, Any] = extract_context(call_or_message=message)
    await bot.set_state(
        user_id=context['user_id'],
        state=states.UserRegistrationStates.registration_password,
    )
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        data["surname"] = context['text']
        main_message_id = data["main_message_id"]
    await bot.delete_message(
        chat_id=context['chat_id'],
        message_id=context['message_id'],
    )
    await send_message(
        bot=bot,
        chat_id=context["chat_id"],
        message_id=main_message_id,
        text="Введите пароль.",
        reply_markup=None,
        is_callback=True,
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_password)
async def registration_user(message: CallbackQuery | Message) -> None:
    """
    Процесс регистрации.
    После ввода пароля пользователя.
    """
    context: Dict[str, Any] = extract_context(call_or_message=message)
    async with bot.retrieve_data(user_id=context['user_id']) as data:
        main_message_id: Any = data["main_message_id"]
        user_info: dict = {
            "name": data["name"],
            "surname": data["surname"],
            "telegram_id": context['user_id'],
            "is_active": True,
            "hashed_password": context['text'],
        }

    response_data: Response = await user_api_client.registration(
        data=user_info,
    )

    if response_data.status_code >= 400:
        await handle_error_api_response(
            response=response_data,
            context=context,
        )
        return

    await bot.delete_message(
        chat_id=context['chat_id'],
        message_id=context['message_id'],
    )

    await bot.delete_state(
            user_id=context['user_id'],
        )
    await send_message(
        bot=bot,
        chat_id=context["chat_id"],
        message_id=main_message_id,
        text="Вы успешно зарегистрированы.",
        reply_markup=inline_keyboard_manager.login(),
        is_callback=True,
    )
