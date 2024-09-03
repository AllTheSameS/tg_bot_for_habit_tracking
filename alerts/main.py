from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.get_all_alert_time import get_all_alert_time_and_telegram_id
from alerts.reminder import reminder
from alerts.reminder_habits import reminder_habits
from typing import List, Tuple, Any


scheduler: AsyncIOScheduler = AsyncIOScheduler()


async def scheduler_start() -> None:
    """
    Функция запуска оповещений.
    При запуске бота добавляет задачи всех имеющиеся в базе данных оповещения.
    """

    scheduler.start()

    scheduler.add_job(
        func=reminder,
        trigger="cron",
        hour=8,
    )

    all_tasks_info: List[Tuple[Any]] | List[None] = (
        await get_all_alert_time_and_telegram_id()
    )

    for telegram_id, job_id, time, habit_title in all_tasks_info:

        if time:
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
