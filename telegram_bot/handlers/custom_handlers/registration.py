from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot.states import states
from settings import settings
from telegram_bot.keyboards.inline.start_keyboard import login_kb
import httpx


@bot.callback_query_handler(func=lambda call: call.data == "registration")
async def cmd_registration(call: CallbackQuery) -> None:
    """Регистрация"""

    await bot.set_state(
        user_id=call.from_user.id,
        state=states.UserRegistrationStates.registration_name,
    )

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Ведите ваше имя.",
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_name)
async def password_registration(message: Message) -> None:
    """Регистрация"""

    await bot.set_state(
        user_id=message.from_user.id,
        state=states.UserRegistrationStates.registration_surname,
    )

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["name"] = message.text

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.id,
    )

    await bot.edit_message_text(
        chat_id=message.chat.id,
        text="Введите вашу фамилию.",
        message_id=message.message_id - 1,
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_surname)
async def password_registration(message: Message) -> None:
    """Регистрация"""

    await bot.set_state(
        user_id=message.from_user.id,
        state=states.UserRegistrationStates.registration_password,
    )

    async with bot.retrieve_data(
        user_id=message.from_user.id,
    ) as data:
        data["surname"] = message.text

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.id,
    )

    await bot.edit_message_text(
        chat_id=message.chat.id,
        text="Введите пароль.",
        message_id=message.message_id - 2,
    )


@bot.message_handler(state=states.UserRegistrationStates.registration_password)
async def registration_user(message: Message) -> None:

    async with bot.retrieve_data(user_id=message.from_user.id) as data:

        user_info: dict = {
            "name": data["name"],
            "surname": data["surname"],
            "telegram_id": message.from_user.id,
            "is_active": True,
            "hashed_password": message.text,
        }

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.base_url}/registration", json=user_info
        )

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.id,
    )

    if response.status_code == 201:

        await bot.edit_message_text(
            chat_id=message.chat.id,
            text="Вы успешно зарегистрированы.\n",
            message_id=message.message_id - 3,
            reply_markup=login_kb(),
        )

        await bot.delete_state(
            user_id=message.from_user.id,
        )

    elif response.status_code == 409:

        await bot.edit_message_text(
            chat_id=message.chat.id,
            text="Пользователь уже существует.",
            message_id=message.message_id - 3,
            reply_markup=login_kb(),
        )

    elif response.status_code >= 500:

        await bot.edit_message_text(
            chat_id=message.chat.id,
            text="Ошибка сервера.",
            message_id=message.message_id - 3,
        )
