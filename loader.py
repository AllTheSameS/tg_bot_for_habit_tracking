"""Модуль конфигурации приложения."""

from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from settings import settings
from fastapi import FastAPI
from api import routes


storage: StateMemoryStorage = StateMemoryStorage()
bot: AsyncTeleBot = AsyncTeleBot(
    token=settings.bot_token,
    state_storage=storage,
)

routers: tuple = (
    routes.get_user_info.get_info_user_router,
    routes.auth_user.auth_router,
    routes.registration_user.registration_router,
    routes.create_habit.create_new_habit_router,
    routes.habit_update.habit_editing_router,
    routes.remove_habit.remove_habit_router,
    routes.get_habit_by_title.get_habit_by_title_router,
    routes.get_all_habits.get_all_habits_router,
    routes.perform_habit.perform_habit_router,
)

app: FastAPI = FastAPI(lifespan=routes.lifespan.lifespan)

for router in routers:
    app.include_router(router=router)
