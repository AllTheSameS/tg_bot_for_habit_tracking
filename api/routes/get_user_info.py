from fastapi import APIRouter, Depends
from schemas.user_schema import UserSchema
from api.routes.auth_user import get_current_token_payload, get_current_active_auth_user

get_info_user_router = APIRouter()


@get_info_user_router.get(
    path="/user_info",
)
async def get_info_user(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "name": user.name,
        "surname": user.surname,
        "logged_in_at": iat,
    }
