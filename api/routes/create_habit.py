from fastapi import APIRouter, Depends
from api.schemas.user_schema import UserSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user

get_info_user_router = APIRouter()


@get_info_user_router.get(
    path="/create_habit",
)
async def create_habit(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    """Создание привычки."""
    pass
