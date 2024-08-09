from fastapi import APIRouter, Depends
from api.schemas.user_schema import UserSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user

get_info_user_router = APIRouter()


@get_info_user_router.post(
    path="/habit/create",
)
async def create_habit(
        habit_info: dict,
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    """Создание привычки."""
    pass
