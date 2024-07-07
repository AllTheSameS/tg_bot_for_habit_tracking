"""
Модуль в котором хранятся все константы.
Attributes:
    DATABASE_URL - Путь к базе данных
    BOT_TOKEN - Токен бота, полученный у @BotFather
    DEFAULT_COMMANDS - Команды поддерживаемые ботом
"""
import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_USER = os.getenv("USER_DB")
DB_PASSWORD = os.getenv("PASSWORD_DB")
DB_NAME = os.getenv("NAME_DB")
DB_HOST = os.getenv("HOST_DB")
DB_PORT = os.getenv("DB_PORT")

BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_COMMANDS = (
    (),
    (),
    (),
)
