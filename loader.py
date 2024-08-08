from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from settings import settings
from fastapi import FastAPI
from api.routes.auth_user import auth_router
from api.routes.lifespan import lifespan
from api.routes.registration_user import registration_router
from api.routes.get_user_info import get_info_user_router


storage = StateMemoryStorage()
bot = AsyncTeleBot(
    token=settings.bot_token,
    state_storage=storage,
)


app = FastAPI(lifespan=lifespan)
app.include_router(router=get_info_user_router)
app.include_router(router=auth_router)
app.include_router(router=registration_router)
