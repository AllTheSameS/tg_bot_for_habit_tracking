"""
Модуль в котором хранятся все константы.
Attributes:
    DATABASE_URL - Путь к базе данных
    BOT_TOKEN - Токен бота, полученный у @BotFather
    DEFAULT_COMMANDS - Команды поддерживаемые ботом
"""
import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import httpx


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    print("Переменные окружения загружены.")


BASE_DIR: Path = Path(__file__).parent


class DbConfig(BaseModel):

    db_dialect: str = os.getenv("DB_DIALECT")
    db_driver: str = os.getenv("DB_DRIVER")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_name: str = os.getenv("DB_NAME")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")

    url: str = f"{db_dialect}+{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Bot(BaseModel):
    default_commands: tuple = (
        ("start", "Старт"),
        ("help", "Вывести справку"),
        ("registration", "Регистрация"),
        ("authorisation", "Вход"),
        ("main_menu", "Главное меню"),
    )


class Settings(BaseSettings):

    base_host: str = os.getenv("BASE_HOST")
    base_port: str = os.getenv("BASE_PORT")
    base_url: str = f"http://{base_host}:{base_port}"
    bot_token: str = os.getenv("BOT_TOKEN")

    auth_jwt: AuthJWT = AuthJWT()
    bot: Bot = Bot()
    db: DbConfig = DbConfig()


client = httpx.AsyncClient()

settings = Settings()
