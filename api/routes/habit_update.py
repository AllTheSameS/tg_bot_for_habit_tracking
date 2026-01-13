from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.habit_schema import HabitSchema
from api.schemas.habit_update_schema import HabitUpdateSchema
from api.routes.auth_user import get_current_active_auth_user, get_current_token_payload
from api.routes.utils.create_alert_time import create_alert_time
from api.database.database import get_async_session
from api.database.crud.habit import habit_crud
from api.database.crud.habit_trackings import habit_trackings_crud
from api.database.models.habit import Habit
from api.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import CompileError
from typing import Dict, List

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
    update_data: HabitUpdateSchema,
    payload: Dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(get_async_session),
) -> HabitSchema:
    """Редактирование привычки."""
    habit: Habit = await habit_crud.get(
        title=habit_title,
        user_id=payload.get("user_id"),
        session=session,
    )

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found.",
        )
    if update_data.title:
        habits: List[str] = [habit.title for habit in user.habits]
        if update_data.title != habit_title and update_data.title in habits:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This name for habit already exists.",
            )
    if not update_data.title and not update_data.description:
        utc_alert_time = create_alert_time(
            alert_time_str=update_data.alert_time,
            user_timezone=user.timezone,
            )
        utc_alert_time: Dict = {'alert_time': utc_alert_time}
        await habit_trackings_crud.update(
                habit_id=habit.id,
                data=utc_alert_time,
                session=session,
            )
        await session.commit()
        return habit
    update_data: Dict = update_data.model_dump(exclude_unset=True, exclude={'alert_time'})
    if update_data:
        try:
            updated_habit: Habit = await habit_crud.update(
                user_id=payload.get("user_id"),
                title=habit_title,
                data=update_data,
                session=session,
            )
            await session.commit()
            return updated_habit

        except CompileError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unconsumed column names.",
            )
