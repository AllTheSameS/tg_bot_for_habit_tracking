from typing import Any
from alerts.reminder_habits import reminder_habits
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerManager:
    @staticmethod
    def update_habit_job(job_id: int, title: str, alert_time: str | datetime, user_id: int, scheduler: AsyncIOScheduler) -> None:
        """Обновление задачи в планировщике."""
        check_job = scheduler.get_job(job_id=str(job_id))
        if alert_time:
            hour, minute = alert_time[:5].split(":")
            if check_job:
                check_job.reschedule(
                    trigger="cron",
                    hour=int(hour),
                    minute=int(minute),
                )
            else:
                scheduler.add_job(
                    id=str(job_id),
                    func=reminder_habits,
                    trigger="cron",
                    hour=int(hour),
                    minute=int(minute),
                    args=(user_id, title),
                )
        else:
            check_job.remove()


scheduler_manager: SchedulerManager = SchedulerManager()