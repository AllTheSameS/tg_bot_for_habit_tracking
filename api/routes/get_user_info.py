from fastapi import APIRouter, Depends, status
from api.schemas.user_schema import UserLoginSchema
from api.schemas.get_user_info_schema import UserInfoSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user

get_info_user_router: APIRouter = APIRouter()


@get_info_user_router.get(
    path="/user_info",
    tags=["GET"],
    description="Displaying information about yourself.",
    response_model=UserInfoSchema,
    responses={
        status.HTTP_200_OK: {
            "model": UserInfoSchema,
            "description": "Displaying information about yourself.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid username or password",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "user inactive",
        },
    },
)
async def get_info_user(
    payload: dict = Depends(get_current_token_payload),
    user: UserLoginSchema = Depends(get_current_active_auth_user),
) -> UserInfoSchema:
    """Вывод информации о пользователе."""
    iat = payload.get("iat")

    return UserInfoSchema(
        name=user.name,
        surname=user.surname,
        logged_in_at=iat,
    )
