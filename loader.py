"""Модуль конфигурации приложения."""
import logging
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from settings import settings, setup_logging
from api import routes


# Настройка логирования при импорте модуля
setup_logging()


storage: StateMemoryStorage = StateMemoryStorage()
bot: AsyncTeleBot = AsyncTeleBot(
    token=settings.bot_token,
    state_storage=storage,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования HTTP запросов."""

    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger('api.http')

        # Логируем входящий запрос
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        try:
            # Выполняем запрос
            response: Response = await call_next(request)

            # Логируем успешный ответ
            logger.info(
                f"Response: {response.status_code} for {request.method} {request.url.path}"
            )

            return response

        except Exception as e:
            # Логируем ошибки
            logger.error(
                f"Error in request {request.method} {request.url.path}: {str(e)}",
                exc_info=True
            )
            raise


routers: tuple = (
    routes.user_update.user_update_router,
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

limiter = Limiter(key_func=get_remote_address)
app: FastAPI = FastAPI(lifespan=routes.lifespan.lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем middleware для логирования
app.add_middleware(LoggingMiddleware)

for router in routers:
    app.include_router(router=router)
