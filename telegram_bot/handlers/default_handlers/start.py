from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot.utils.extract_context import extract_context
from telegram_bot.keyboards.inline_keyboards import inline_keyboard_manager
from typing import Dict


@bot.message_handler(commands=["start"])
async def cmd_start(message: Message | CallbackQuery) -> None:
    """Инициализация диалога с ботом"""
    context: Dict = extract_context(call_or_message=message)
    welcome_text: str = """👋 Добро пожаловать в мир осознанных привычек!

    Каждый день — это кирпичик в фундаменте твоей будущей жизни. Я здесь, чтобы помочь тебе строить его осознанно и последовательно.

    **Что я умею:**
    • 📅 **Трекать привычки** — отмечай выполнение каждый день.
    • 🔔 **Напоминать** — чтобы ты ничего не забыл в потоке дня.

    **С чего начать?**
    1. Используй команду /create_habit, чтобы добавить новую привычку (например, "Пить воду", "Читать 20 минут", "Зарядка").
    2. Каждый день отмечай её выполнение.
    3. Установи время оповещения, чтобы не забыть выполнить привычку.

    Маленькие шаги ведут к большим переменам. Начнем? ✨"""
    await bot.send_message(
        chat_id=context['chat_id'],
        text=welcome_text,
        reply_markup=inline_keyboard_manager.registration_or_login(),
    )
