### Название проекта:
    Чат-бот трекинга привычек.

### Основные функции приложения:
* Добавление и удаление привычек, полный функционал по редактированию.
* Функция фиксации выполнения привычки.
* Напоминание о необходимости выполнить привычку, в установленное пользователем время.
* REST API для управления пользователями и привычками.
* JWT аутентификация с refresh tokens.
* Ежедневные напоминания всем пользователям.

### Архитектура:
Проект состоит из:
- **FastAPI backend**: REST API для пользователей и привычек.
- **Telegram bot**: Интерфейс для взаимодействия с пользователями.
- **PostgreSQL**: Основная база данных для API.
- **SQLite**: База для токенов бота.
- **APScheduler**: Планировщик напоминаний.

### Технологический стек:
* Poetry.
* PostgreSQL.
* SQLite.
* httpx.
* SQLAlchemy.
* PytelegramBotAPI.
* FastAPI.
* PyJWT.
* APScheduler.
* Docker-compose.
* SlowAPI (rate limiting).
* CORS middleware.

### API Документация:
После запуска доступна по адресу: http://localhost:8000/docs

### Основные эндпоинты:
- `POST /login` - Авторизация, возвращает access и refresh tokens.
- `POST /refresh` - Обновление access token.
- `GET /user/info` - Информация о пользователе.
- `POST /habit` - Создание привычки.
- `GET /habits` - Список привычек пользователя.
- `PATCH /habit/perform/{title}` - Отметка выполнения привычки.

### Запуск:
* Создать в корне проекта папку 'certs'.
  * В папке 'certs' создать публичный, приватный ключ:

        openssl genrsa -out jwt-private.pem 2048
        openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

* Создать файл '.env' и заполнить его по примеру файла '.env.template'.
  * Подгрузить все библиотеки из pyproject.toml командой:

        poetry install

* Запускаем проект:

      docker compose up

### Переменные окружения:
См. .env.template для полного списка.

### Логирование:
Логи пишутся в logs/app.log с ротацией (макс 10MB, 5 бэкапов).
