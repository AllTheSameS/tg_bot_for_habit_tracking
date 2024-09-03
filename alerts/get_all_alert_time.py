from api.database.models.habit_trackings import HabitTrackings
from api.database.models.user import User
from api.database.models.habit import Habit
from api.database.database import async_session
from sqlalchemy import select, Subquery
from typing import List, Tuple, Any


async def get_all_alert_time_and_telegram_id() -> List[Tuple[Any]]:
    """
    Получения телеграм ID пользователя,
    время оповещения, ID и названия привычки
    для добавления задач оповещения.
    """

    async with async_session() as session:
        subquery: Subquery = (
            select(
                Habit.id.label("habit_id"),
                Habit.title.label("habit_title"),
                User.telegram_id.label("telegram_id"),
            )
            .join(
                User,
                User.id == Habit.user_id,
            )
            .subquery()
        )

        all_alert_time: Any = await session.execute(
            select(
                subquery.c.telegram_id,
                HabitTrackings.id,
                HabitTrackings.alert_time,
                subquery.c.habit_title,
            ).where(HabitTrackings.id == subquery.c.habit_id)
        )

    return all_alert_time.all()
