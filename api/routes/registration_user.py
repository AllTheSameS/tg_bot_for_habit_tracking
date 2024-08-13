from api.database.models.user import User
from api.database.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from api.schemas.user_schema import UserSchema
from api.auth.utils import hash_password

registration_router = APIRouter()


@registration_router.post(
    path="/registration",
    response_model=UserSchema,
    tags=["Registration"],
    description="User registration",
)
async def registration_user(
        user_info: UserSchema,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание пользователя."""

    new_user = User(
        telegram_id=user_info.telegram_id,
        name=user_info.name,
        surname=user_info.surname,
        hashed_password=hash_password(user_info.hashed_password),
    )

    session.add(new_user)
    await session.commit()

    return new_user





