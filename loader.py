from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from settings import settings
from fastapi import FastAPI
from api import routes


storage = StateMemoryStorage()
bot = AsyncTeleBot(
    token=settings.bot_token,
    state_storage=storage,
)


app = FastAPI(lifespan=routes.lifespan.lifespan)
app.include_router(router=routes.get_user_info.get_info_user_router)
app.include_router(router=routes.auth_user.auth_router)
app.include_router(router=routes.registration_user.registration_router)
app.include_router(router=routes.create_habit.create_new_habit_router)
app.include_router(router=routes.habit_editing.habit_editing_router)
app.include_router(router=routes.remove_habit.remove_habit_router)
app.include_router(router=routes.get_habit_by_title_or_id.get_habit_by_title_or_id_router)
app.include_router(router=routes.get_all_habits.get_all_habits_router)
app.include_router(router=routes.perform_habit.perform_habit_router)
