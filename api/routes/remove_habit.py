from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.user_schema import UserLoginSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.database.database import get_async_session
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from api.routes.utils.get_habit_by_title import get_habit_by_title
from sqlalchemy.ext.asyncio import AsyncSession

remove_habit_router = APIRouter()


@remove_habit_router.delete(
    path="/habit/remove/{habit_title}",
    tags=["DELETE"],
    description="Deleting a habit",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Habit removed.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "token invalid (user not found)",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Habit not found.",
        },
    },
)
async def remove_habit(
    habit_title: str,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Удаление привычки."""

    habit: Habit = await get_habit_by_title(
        habit_title=habit_title,
        session=session,
        user_id=payload.get("user_id"),
    )

    if habit:
        await session.delete(habit)
        await session.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found."
        )
