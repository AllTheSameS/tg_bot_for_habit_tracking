import logging
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from api.schemas.new_habit_schema import NewHabitSchemaIn, NewHabitSchemaOut
from api.database.crud.habit import habit_crud
from api.database.crud.habit_trackings import habit_trackings_crud
from api.database.models.habit import Habit
from api.database.models.habit_trackings import HabitTrackings
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user
from api.routes.utils.create_alert_time import create_alert_time
from api.database.database import get_async_session
from api.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict


create_new_habit_router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger('api.routes.create_habit')


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
    payload: Dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(get_async_session),
) -> NewHabitSchemaOut:
    """Создание привычки."""
    logger.info(f"Создание привычки '{habit_info.title}' для пользователя {user.id}")
    try:
        habit = await habit_crud.get(
            title=habit_info.title,
            user_id=payload.get("user_id"),
            session=session,
        )

        if habit:
            logger.warning(f"Попытка создать существующую привычку '{habit_info.title}' для пользователя {user.id}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A habit with this name already exists.",
            )
        new_habit: Habit = await habit_crud.create(
            title=habit_info.title,
            description=habit_info.description,
            user_id=user.id,
            session=session,
        )

        session.add(new_habit)
        await session.flush()

        if habit_info.alert_time and user.timezone:
            habit_info.alert_time = create_alert_time(
                alert_time_str=habit_info.alert_time,
                user_timezone=user.timezone,
                )
        new_habit_tracking: HabitTrackings = await habit_trackings_crud.create(
            habit_id=new_habit.id,
            alert_time=habit_info.alert_time,
            session=session,
        )
        session.add(new_habit_tracking)
        await session.refresh(new_habit)
        new_habit.habits_tracking.append(new_habit_tracking)
        await session.commit()
        return new_habit

    except ValueError as e:
        logger.error(f"Ошибка валидации при создании привычки '{habit_info.title}' для пользователя {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании привычки '{habit_info.title}' для пользователя {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL_SERVER_ERROR.",
        )
