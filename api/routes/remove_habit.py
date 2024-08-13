from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.user_schema import UserSchema
from api.schemas.habit_editing import HabitEditingSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.database.database import get_async_session
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from api.routes.utils.get_habit_by_title_or_id import get_habit_by_title_or_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

remove_habit_router = APIRouter()


@remove_habit_router.post(
    path="/habit/remove",
    tags=["POST"],
    description="Deleting a habit",
)
async def remove_habit(
        habit_title_or_id: str | int,
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление привычки."""

    habit = await get_habit_by_title_or_id(
        habit_title_or_id=habit_title_or_id,
        session=session,
    )

    await session.delete(habit)
    await session.commit()

    return {f"Привычка '{habit.title}' удалена."}, 200
