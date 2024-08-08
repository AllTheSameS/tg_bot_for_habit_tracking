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

    _db_dialect: str = os.getenv("DB_DIALECT")
    _db_driver: str = os.getenv("DB_DRIVER")
    _db_user: str = os.getenv("DB_USER")
    _db_password: str = os.getenv("DB_PASSWORD")
    _db_name: str = os.getenv("DB_NAME")
    _db_host: str = os.getenv("DB_HOST")
    _db_port: str = os.getenv("DB_PORT")

    url: str = f"{_db_dialect}+{_db_driver}://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"


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
    sqlite_db: DBLiteConfig = DBLiteConfig()


client = httpx.AsyncClient()

settings = Settings()
