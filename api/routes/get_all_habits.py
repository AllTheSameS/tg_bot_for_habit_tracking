from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user_schema import UserSchema
from api.schemas.habit_info_schema import HabitInfoSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.database.database import get_async_session
from api.database.models.habit import Habit
from sqlalchemy import select


get_all_habits_router = APIRouter()


@get_all_habits_router.get(
    path="/habit/all",
    tags=["GET"],
    description="Displaying all habits",
)
async def get_all_habits(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Вывод всех привычек."""

    habits = await session.execute(
        select(
            Habit
        ).filter(
            Habit.user_id == payload.get("sub"),
        )
    )

    return habits.scalars().all()
