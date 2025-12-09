from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.new_habit_schema import NewHabitSchemaIn, NewHabitSchemaOut
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.routes.utils.get_habit_by_title import get_habit_by_title
from api.routes.utils.create_alert_time import create_alert_time
from api.database.database import get_async_session
from api.database.models.habit import Habit
from api.database.models.user import User
from api.database.models.habit_trackings import HabitTrackings
from sqlalchemy.ext.asyncio import AsyncSession


create_new_habit_router: APIRouter = APIRouter()


@create_new_habit_router.post(
    path="/habit/create",
    tags=["POST"],
    description="Creating a new habit",
    response_model=NewHabitSchemaOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Creating a new habit.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid time format.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token error.",
        },
        status.HTTP_409_CONFLICT: {
            "description": "A habit with this name already exists.",
        },
    },
)
async def create_habit(
    habit_info: NewHabitSchemaIn,
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(get_async_session),
) -> NewHabitSchemaOut:
    """Создание привычки."""
    try:
        check_habit_title: Habit = await get_habit_by_title(
            habit_title=habit_info.title,
            user_id=payload.get("user_id"),
            session=session,
        )

        if check_habit_title:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A habit with this name already exists.",
            )

        new_habit: Habit = Habit(
            title=habit_info.title,
            user_id=user.id,
            description=habit_info.description,
        )

        session.add(new_habit)
        await session.flush()

        if habit_info.alert_time and user.timezone:
            habit_info.alert_time = create_alert_time(
                alert_time_str=habit_info.alert_time,
                user_timezone=user.timezone,
                )

        new_habit_tracking: HabitTrackings = HabitTrackings(
            habit_id=new_habit.id,
            alert_time=habit_info.alert_time,
        )

        session.add(new_habit_tracking)
        await session.refresh(new_habit)
        await session.commit()

        return new_habit

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL_SERVER_ERROR.",
        )