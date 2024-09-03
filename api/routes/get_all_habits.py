from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.habit_schema import HabitSchema
from api.routes.auth_user import get_current_token_payload
from api.database.database import get_async_session
from api.database.models.habit import Habit
from sqlalchemy import select, Result, Sequence
from typing import List


get_all_habits_router: APIRouter = APIRouter()


@get_all_habits_router.get(
    path="/habit/all",
    tags=["GET"],
    description="Displaying all habits.",
    response_model=List[HabitSchema],
    responses={
        status.HTTP_200_OK: {
            "model": List[HabitSchema],
            "description": "Displaying all habits.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": [
                "invalid username or password",
                "invalid token error.",
            ]
        },
    },
)
async def get_all_habits(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence:
    """Вывод всех привычек."""

    habits: Result = await session.execute(
        select(
            Habit,
        ).filter(
            Habit.user_id == payload.get("user_id"),
        )
    )

    return habits.scalars().all()
