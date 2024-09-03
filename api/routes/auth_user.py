"""
Модуль аутентификации пользователя.
"""

from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status
from jwt import InvalidTokenError
from api.schemas import user_schema
from api.schemas import token_schema
from fastapi.exceptions import HTTPException
from api.auth.utils import validate_password, encode_jwt, decode_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_async_session
from sqlalchemy import select
from api.database.models.user import User
from typing import Any

auth_router: APIRouter = APIRouter()

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl="/login",
)


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """Функция декодинга токена."""
    try:

        payload: dict = decode_jwt(
            token=token,
        )

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error.",
        )

    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> user_schema.UserLoginSchema:
    """Функция проверки зарегистрирован ли пользователь."""

    user: Any = await session.execute(
        select(User).filter(User.telegram_id == payload.get("telegram_id"))
    )

    if user := user.one_or_none()[0]:
        return user_schema.UserLoginSchema(
            id=user.id,
            name=user.name,
            surname=user.surname,
            is_active=user.is_active,
            telegram_id=user.telegram_id,
            hashed_password=user.hashed_password,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_active_auth_user(
    user: user_schema.UserLoginSchema = Depends(get_current_auth_user),
) -> user_schema.UserLoginSchema:
    """Функция проверки активности пользователя."""

    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def validate_auth_user(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    """Функция авторизации пользователя."""
    user = await session.execute(
        select(User).filter(User.telegram_id == int(user_form.username))
    )

    try:

        user = user.one_or_none()[0]

    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )

    if not validate_password(
        password=user_form.password,
        hashed_password=user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


@auth_router.post(
    "/login",
    response_model=token_schema.TokenSchemas,
    tags=["Authorization"],
    description="User authorization.",
    responses={
        status.HTTP_200_OK: {
            "model": token_schema.TokenSchemas,
            "description": "the user has been successfully authorized.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid username or password",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "user inactive",
        },
        status.HTTP_404_NOT_FOUND: {"description": "user not found."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "internal server error."
        },
    },
)
async def auth_user_issue_jwt(
    user: user_schema.UserLoginSchema = Depends(validate_auth_user),
) -> token_schema.TokenSchemas:
    """Cоздание JWT токена."""

    payload: dict = {
        "user_id": user.id,
        "telegram_id": user.telegram_id,
        "name": user.name,
        "surname": user.surname,
    }

    token: str = encode_jwt(payload=payload)

    return token_schema.TokenSchemas(
        access_token=token,
        token_type="Bearer",
    )
