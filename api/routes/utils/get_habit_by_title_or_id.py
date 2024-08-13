from fastapi import status
from fastapi.exceptions import HTTPException
from api.database.models.habit import Habit
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.exc import NoResultFound


async def get_habit_by_title_or_id(
        habit_title_or_id: str | int,
        session: AsyncSession,
):
    """Функция вывода привычки по названию или ID"""
    arg = Habit.id

    try:

        habit_title_or_id = int(habit_title_or_id)

    except ValueError:
        arg = Habit.title

    try:

        habit = await session.execute(
            select(
                Habit
            ).filter(
                arg == habit_title_or_id
            )
        )

        habit = habit.one()[0]

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habits with this name not found."
        )

    return habit




