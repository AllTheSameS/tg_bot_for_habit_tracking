from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.user_schema import UserSchema
from api.schemas.habit_editing import HabitEditingSchema
from api.schemas.new_habit import NewHabitSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.routes.utils.get_habit_by_title_or_id import get_habit_by_title_or_id
from api.database.database import get_async_session
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.exc import CompileError
import datetime

habit_editing_router = APIRouter()


@habit_editing_router.patch(
    path="/habit/editing",
    tags=["PATCH"],
    description="Changing a habit",
)
async def habit_editing(
        habit_info: HabitEditingSchema,
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Редактирование привычки."""

    habit = await get_habit_by_title_or_id(
        habit_title_or_id=habit_info.title,
        session=session,
    )

    if habit_info.title_field == "alert_time":

        try:

            hour, minutes = habit_info.new_info.split(':')

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Enter the correct alert time. For example, 07:00.",
            )

        try:

            await session.execute(
                update(
                    HabitTrackings
                ).filter(
                    HabitTrackings.habit_id == habit.id
                ).values(
                    {habit_info.title_field: datetime.time(hour=int(hour), minute=int(minutes))}
                )
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=exc.args,
            )

        result = {f"Новое время оповещения привычки '"
                  f"{habit_info.title}': "
                  f"{str(hour).zfill(2)}:{str(minutes).zfill(2)}"}, 200

    else:

        try:
            result = await session.execute(
                update(
                    Habit
                ).filter(
                    Habit.title == habit_info.title
                ).values(
                    {habit_info.title_field: habit_info.new_info}
                ).returning(
                    Habit
                )
            )

            await session.commit()

            new_habit = result.one()[0]

            result = NewHabitSchema(
                title=new_habit.title,
                description=new_habit.description,
            ), 200

        except CompileError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unconsumed column names: {habit_info.title_field}",
            )

    return result
