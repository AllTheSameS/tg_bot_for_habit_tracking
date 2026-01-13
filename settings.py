"""
Модуль хранения констант.
"""

import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    print("Переменные окружения загружены.")


BASE_DIR: Path = Path(__file__).parent


class DbConfig(BaseModel):

    _db_dialect: str = os.getenv("DB_DIALECT")
    _db_driver: str = os.getenv("DB_DRIVER")
    _db_user: str = os.getenv("DB_USER")
    _db_password: str = os.getenv("DB_PASSWORD")
    _db_name: str = os.getenv("DB_NAME")
    _db_host: str = os.getenv("DB_HOST")
    _db_port: str = os.getenv("DB_PORT")

    url: str = (
        f"{_db_dialect}+{_db_driver}://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"
    )


class DBLiteConfig(BaseModel):
    _db_dialect: str = os.getenv("DB_SQLITE_DIALECT")
    _db_driver: str = os.getenv("DB_SQLITE_DRIVER")
    _db_path: str = os.getenv("DB_SQLITE_PATH")
    _db_name: str = os.getenv("DB_SQLITE_NAME")

    url: str = f"{_db_dialect}+{_db_driver}://{_db_path}/{_db_name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Bot(BaseModel):
    default_commands: tuple = (
        ("start", "Старт"),
        ("help", "Вывести справку"),
        ("create_habit", "Создать привычку"),
        ("my_habits", "Мои привычки"),
    )


class LoggingConfig(BaseModel):
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    json_format: bool = os.getenv("LOG_JSON_FORMAT", "false").lower() == "true"
    file_path: str = os.getenv("LOG_FILE_PATH", "logs/app.log")

    def get_level(self) -> int:
        return getattr(logging, self.level.upper(), logging.INFO)


class Settings(BaseSettings):

    base_host: str = os.getenv("BASE_HOST")
    base_port: str = os.getenv("BASE_PORT")
    base_url: str = f"http://{base_host}:{base_port}"
    bot_token: str = os.getenv("BOT_TOKEN")
    daily_reminder: str = os.getenv("DAILY_REMINDER")

    auth_jwt: AuthJWT = AuthJWT()
    bot: Bot = Bot()
    db: DbConfig = DbConfig()
    sqlite_db: DBLiteConfig = DBLiteConfig()
    logging: LoggingConfig = LoggingConfig()


settings: Settings = Settings()


def setup_logging() -> None:
    """Настройка логирования для всего приложения."""
    # Создаем директорию для логов если не существует
    log_dir = Path(settings.logging.file_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Базовая конфигурация
    logging.basicConfig(
        level=settings.logging.get_level(),
        format=settings.logging.format,
        handlers=[
            logging.StreamHandler(sys.stdout),  # Логи в консоль
            RotatingFileHandler(settings.logging.file_path, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'),  # Ротация логов
        ]
    )

    # Настройка логгеров для разных модулей
    loggers_config = {
        'api': logging.INFO,
        'telegram_bot': logging.INFO,
        'database': logging.WARNING,  # Меньше шума от БД
        'scheduler': logging.INFO,
        'httpx': logging.WARNING,  # Меньше шума от HTTP клиентов
        'sqlalchemy': logging.WARNING,  # Меньше шума от SQLAlchemy
    }

    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

    # Логгер для основного приложения
    app_logger = logging.getLogger('app')
    app_logger.info("Логирование настроено успешно")
