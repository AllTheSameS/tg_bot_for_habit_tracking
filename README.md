### Название проекта:
    Чат-бот трекинга привычек.

### Основные функции приложения:
* Добавление и удаление привычек, полный функционал по редактированию.
* Функция фиксации выполнения привычки.
* Напоминание о необходимости выполнить привычку, в установленное пользователем время. 

### Технологический стек:
* Poetry.
* PostgreSQL.
* Sqlite
* httpx
* SQLAlchemy.
* PytelegramBotAPI.
* FastAPI.
* PyJWT.
* Apscheduler.
* Docker-compose.

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
