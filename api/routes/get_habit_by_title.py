from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.habit import Habit
from api.schemas.habit_schema import HabitSchema
from api.routes.auth_user import get_current_token_payload
from api.routes.utils.get_habit_by_title import get_habit_by_title
from api.database.database import get_async_session


get_habit_by_title_router: APIRouter = APIRouter()


@get_habit_by_title_router.get(
    path="/habit/title/{habit_title}",
    tags=["GET"],
    description="Displaying a habit by title.",
    response_model=HabitSchema,
    responses={
        status.HTTP_200_OK: {
            "model": HabitSchema,
            "description": "Displaying a habit by title.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid username or password.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Habit not found.",
        },
    },
)
async def get_habit_title(
    habit_title: str,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> HabitSchema:
    """Вывод привычки по названию."""

    habit: Habit = await get_habit_by_title(
        habit_title=habit_title,
        user_id=payload.get("user_id"),
        session=session,
    )

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found.",
        )

    else:

        return habit
