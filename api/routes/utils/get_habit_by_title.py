from api.database.models.habit import Habit
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, CursorResult


async def get_habit_by_title(
    habit_title: str,
    user_id: int,
    session: AsyncSession,
) -> Habit:
    """Функция вывода привычки пользователя по названию."""

    habit: Result | CursorResult = await session.execute(
        select(Habit).filter(
            Habit.user_id == user_id,
            Habit.title == habit_title,
        )
    )

    return habit.scalar_one_or_none()
