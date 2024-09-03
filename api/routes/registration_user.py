from api.database.models.user import User
from api.database.database import get_async_session
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from api.schemas.user_schema import UserRegistrationSchema
from api.auth.utils import hash_password
from sqlalchemy.exc import IntegrityError

registration_router: APIRouter = APIRouter()


@registration_router.post(
    path="/registration",
    response_model=UserRegistrationSchema,
    tags=["Registration"],
    description="User registration.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserRegistrationSchema,
            "description": "User registration",
        },
        status.HTTP_409_CONFLICT: {
            "description": "User already exists.",
        },
    },
)
async def registration_user(
    user_info: UserRegistrationSchema,
    session: AsyncSession = Depends(get_async_session),
) -> UserRegistrationSchema:
    """Создание пользователя."""
    try:
        new_user: User = User(
            telegram_id=user_info.telegram_id,
            name=user_info.name,
            surname=user_info.surname,
            hashed_password=hash_password(user_info.hashed_password),
        )

        session.add(new_user)
        await session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )

    return new_user
