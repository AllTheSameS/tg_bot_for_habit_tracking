from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.habit_schema import HabitSchema
from api.schemas.habit_update_schema import HabitUpdateSchema
from api.routes.auth_user import get_current_token_payload
from api.routes.utils.get_habit_by_title import get_habit_by_title
from api.database.database import get_async_session
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from sqlalchemy.exc import CompileError

import pytz
import datetime

habit_editing_router: APIRouter = APIRouter()


@habit_editing_router.patch(
    path="/habit/update/{habit_title}",
    tags=["PATCH"],
    description="Changing a habit.",
    response_model=HabitSchema,
    responses={
        status.HTTP_200_OK: {
            "description": "Changing a habit.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Enter the correct alert time. For example, 07:00.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid username or password.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": ["Unconsumed column names.", "Habit not found."],
        },
        status.HTTP_409_CONFLICT: {
            "description": "A habit with this name already exists.",
        },
    },
)
async def habit_update(
    habit_title: str,
    habit_info: HabitUpdateSchema,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> HabitSchema:
    """Редактирование привычки."""

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

    if habit_info.title:

        check_title_habit: Habit = await get_habit_by_title(
            habit_info.title,
            user_id=payload.get("user_id"),
            session=session,
        )

        if check_title_habit:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This name for habit already exists.",
            )

    new_info: dict = habit_info.model_dump(exclude_unset=True, exclude={"alert_time"})

    if habit_info.alert_time:

        try:

            habit_info.alert_time = datetime.datetime.strptime(
                habit_info.alert_time,
                "%H:%M",
            ).replace(
                tzinfo=pytz.timezone(
                    "Asia/Novosibirsk",
                )
            )

        except ValueError:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time format.",
            )

        await session.execute(
            update(
                HabitTrackings,
            )
            .where(
                HabitTrackings.habit_id == habit.id,
            )
            .values(
                {"alert_time": habit_info.alert_time},
            )
        )

        await session.flush()

    if new_info:
        try:

            new_habit = await session.execute(
                update(
                    Habit,
                )
                .where(
                    Habit.user_id == payload.get("user_id"),
                    Habit.title == habit_title,
                )
                .values(
                    **new_info,
                )
                .returning(
                    Habit,
                )
            )

            await session.commit()

            return new_habit.scalar()

        except CompileError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unconsumed column names.",
            )

    else:
        new_habit = await session.execute(
            select(Habit).where(
                Habit.user_id == payload.get("user_id"),
                Habit.title == habit_title,
            )
        )

        return new_habit.scalar()
