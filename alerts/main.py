import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.get_all_alert_time import get_all_alert_time_and_telegram_id
from alerts.reminder import reminder
from alerts.reminder_habits import reminder_habits
from typing import List, Tuple, Any
from settings import settings

logger = logging.getLogger('scheduler')
scheduler: AsyncIOScheduler = AsyncIOScheduler()


async def scheduler_start() -> None:
    """
    Функция запуска оповещений.
    При запуске бота добавляет задачи всех имеющиеся в базе данных оповещения.
    """
    logger.info("Запуск планировщика уведомлений")

    try:
        scheduler.start()
        logger.info("Планировщик APScheduler запущен")

        logger.info(f"Добавление ежедневного напоминания в {settings.daily_reminder}:00")
        scheduler.add_job(
            func=reminder,
            trigger="cron",
            hour=int(settings.daily_reminder),
        )

        logger.info("Загрузка существующих задач из базы данных")
        all_tasks_info: List[Tuple[Any]] | List[None] = (
            await get_all_alert_time_and_telegram_id()
        )

        logger.info(f"Найдено {len(all_tasks_info)} задач для планирования")
        for telegram_id, job_id, time, habit_title in all_tasks_info:
            if time and time != 'Не установлено.':
                logger.debug(f"Добавление задачи для пользователя {telegram_id}: '{habit_title}' на {time}")
                scheduler.add_job(
                    id=str(job_id),
                    func=reminder_habits,
                    trigger="cron",
                    hour=time.hour,
                    minute=time.minute,
                    args=(
                        telegram_id,
                        habit_title,
                    ),
                )
            else:
                logger.warning(f"Пропуск задачи для пользователя {telegram_id}: '{habit_title}' - время не установлено")

        logger.info("Все задачи планировщика загружены")

    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {str(e)}", exc_info=True)
        raise
