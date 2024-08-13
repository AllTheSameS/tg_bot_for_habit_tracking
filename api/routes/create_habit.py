from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.user_schema import UserSchema
from api.schemas.habit_info_schema import HabitInfoSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.database.database import get_async_session
from api.database.models.user import User
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime

create_new_habit_router = APIRouter()


@create_new_habit_router.post(
    path="/habit/create",
    tags=["POST"],
    description="Creating a new habit",
)
async def create_habit(
        habit_info: HabitInfoSchema,
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Создание привычки."""

    telegram_id = 0

    user_id = await session.execute(
        select(
            User
        ).filter(
            User.telegram_id == telegram_id
        )
    )

    if user_id := user_id.one_or_none():
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no user with this ID in the database.",
            )

        else:
            user_id = user_id[0].id

    check_habit_title = await session.execute(
        select(
            Habit
        ).filter(
            Habit.title == habit_info.title
        )
    )

    if check_habit_title.one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A habit with this name already exists.",
        )

    else:
        new_habit = Habit(
            title=habit_info.title,
            user_id=user_id,
            description=habit_info.description,
        )

        session.add(new_habit)
        await session.flush()

        hour, minutes = habit_info.alert_time.split(':')

        new_habit_tracking = HabitTrackings(
            habit_id=new_habit.id,
            alert_time=datetime.time(
                hour=int(hour),
                minute=int(minutes),
            )
        )

        session.add(new_habit_tracking)
        await session.commit()

        return f"Привычка {new_habit.title} успешно добавлена."
