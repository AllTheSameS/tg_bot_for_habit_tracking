from fastapi import APIRouter, Depends, status
from api.schemas.user_update_schema import UserUpdateSchemaIn, UserUpdateSchemaOut
from api.routes.auth_user import get_current_token_payload
from api.database.database import get_async_session
from api.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


user_update_router: APIRouter = APIRouter()


@user_update_router.patch(
    path="/me",
    tags=["PATCH"],
    description="Update user info.",
    response_model=UserUpdateSchemaOut,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful update.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "...",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "...",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found.",
        },
    },
)
async def update_user(
    update_data: UserUpdateSchemaIn,
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> UserUpdateSchemaOut:
    """Редактирование пользователя."""
    user = await session.get(User, payload['user_id'])
    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        if hasattr(user, field):
            setattr(user, field, value)
    await session.commit()

    return UserUpdateSchemaOut.model_validate(user)
