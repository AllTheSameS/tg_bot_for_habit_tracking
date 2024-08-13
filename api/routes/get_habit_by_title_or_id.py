from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.user_schema import UserSchema
from api.schemas.habit_info_schema import HabitInfoSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.routes.utils.get_habit_by_title_or_id import get_habit_by_title_or_id
from api.database.database import get_async_session


get_habit_by_title_or_id_router = APIRouter()


@get_habit_by_title_or_id_router.get(
    path="/habit/title_or_id",
    tags=["GET"],
    description="Displaying a habit by name or ID",
)
async def get_habit_title_or_id(
        habit_title: str | int,
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Вывод привычки по названию или по ID."""

    habit = await get_habit_by_title_or_id(
        habit_title_or_id=habit_title,
        session=session,
    )

    return HabitInfoSchema(
        title=habit.title,
        description=habit.description,
        alert_time=habit.habits_tracking[0].alert_time,
        count=habit.habits_tracking[0].count,
    )
