import logging
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from sqlalchemy import Result, update
from datetime import datetime


class CRUDHabitTracking:
    def __init__(self):
        self.logger = logging.getLogger('database.crud.habit_trackings')

    async def create(self, habit_id: int, alert_time: datetime | None, session: AsyncSession) -> HabitTrackings:
        self.logger.debug(f"Создание трекинга для привычки {habit_id}")
        try:
            new_tracking = HabitTrackings(
                habit_id=habit_id,
                alert_time=alert_time,
            )
            session.add(new_tracking)
            self.logger.debug(f"Трекинг для привычки {habit_id} добавлен в сессию")
            return new_tracking
        except Exception as e:
            self.logger.error(f"Ошибка при создании трекинга для привычки {habit_id}: {str(e)}", exc_info=True)
            raise

    async def get(self, habit_id: int, session: AsyncSession) -> Habit:
        pass

    async def update(self, habit_id: int, data: Dict, session: AsyncSession) -> Result:
        habit_trackings: Result = await session.execute(
            update(
                HabitTrackings,
            )
            .where(
                HabitTrackings.habit_id == habit_id,
            )
            .values(
                data,
            )
        )
        return habit_trackings

    async def delete_alert_time(self, session: AsyncSession) -> None:
        pass



habit_trackings_crud: CRUDHabitTracking = CRUDHabitTracking()
