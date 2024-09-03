from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from api.database.models.habit import Habit
from api.schemas.habit_schema import HabitSchema
from api.routes.auth_user import get_current_token_payload
from api.database.database import get_async_session
from api.routes.utils.get_habit_by_title import get_habit_by_title
from sqlalchemy.ext.asyncio import AsyncSession


perform_habit_router: APIRouter = APIRouter()


@perform_habit_router.patch(
    path="/habit/perform/{title}",
    tags=["DELETE"],
    description="Fixation of habit execution.",
    responses={
        status.HTTP_200_OK: {
            "model": HabitSchema,
            "description": "Fixation of habit execution.",
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "Habit removed.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token error.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Habit not found.",
        },
    },
)
async def perform_habit(
    title: str,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> HabitSchema | None:
    """Выполнение привычки."""

    habit: Habit = await get_habit_by_title(
        habit_title=title,
        session=session,
        user_id=payload.get("user_id"),
    )

    if habit:
        habit.habits_tracking[0].count -= 1

        if habit.habits_tracking[0].count < 1:
            await session.delete(habit)
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="Habit removed.",
            )

        else:
            return habit

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found.",
        )
