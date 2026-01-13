"""
Модуль аутентификации пользователя.
"""

from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status
from jwt import InvalidTokenError
from api.schemas import token_schema, payload_schema
from fastapi.exceptions import HTTPException
from api.auth.utils import validate_password, encode_jwt, decode_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_async_session
from api.database.crud.user import user_crud
from api.database.models.user import User
from settings import settings
from typing import Dict

auth_router: APIRouter = APIRouter()

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl="/login",
)


async def get_current_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Dict:
    """Функция декодинга токена."""
    try:

        payload: Dict = decode_jwt(
            token=token,
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error.",
        )

    return payload


async def get_current_auth_user(
    payload: Dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Функция проверки зарегистрирован ли пользователь."""
    user: User = await user_crud.get_user(
        user_id=payload.get("telegram_id"),
        session=session,
    )

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found).",
    )


async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
) -> User:
    """Функция проверки активности пользователя."""

    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def validate_auth_user(
    user_form = Depends(OAuth2PasswordRequestForm),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Функция авторизации пользователя."""
    try:
        user: User = await user_crud.get_user(
            user_id=int(user_form.username),
            session=session,
        )
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.",
        )

    if not validate_password(
        password=user_form.password,
        hashed_password=user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive.",
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
    user: User = Depends(validate_auth_user),
) -> token_schema.TokenSchemas:
    """Cоздание JWT токенов."""
    payload: payload_schema.PayloadSchema = payload_schema.PayloadSchema(
        user_id=user.id,
        telegram_id=user.telegram_id,
        name=user.name,
        surname=user.surname,
        timezone=user.timezone,
        habits=user.habits,
    )
    access_token: str = encode_jwt(payload=payload.model_dump())
    refresh_token: str = encode_jwt(
        payload={"sub": str(user.telegram_id)},
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )
    return token_schema.TokenSchemas(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


@auth_router.post(
    "/refresh",
    response_model=token_schema.TokenSchemas,
    tags=["Authorization"],
    description="Refresh access token.",
    responses={
        status.HTTP_200_OK: {
            "model": token_schema.TokenSchemas,
            "description": "Tokens refreshed successfully.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid refresh token",
        },
    },
)
async def refresh_access_token(
    refresh_data: token_schema.RefreshTokenSchema,
    session: AsyncSession = Depends(get_async_session),
) -> token_schema.TokenSchemas:
    """Обновление access токена с помощью refresh токена."""
    try:
        payload: Dict = decode_jwt(token=refresh_data.refresh_token)
        telegram_id: str = payload.get("sub")
        if not telegram_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        )

    user: User = await user_crud.get_user(user_id=int(telegram_id), session=session)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive.",
        )

    payload: payload_schema.PayloadSchema = payload_schema.PayloadSchema(
        user_id=user.id,
        telegram_id=user.telegram_id,
        name=user.name,
        surname=user.surname,
        timezone=user.timezone,
        habits=user.habits,
    )
    access_token: str = encode_jwt(payload=payload.model_dump())
    refresh_token: str = encode_jwt(
        payload={"sub": str(user.telegram_id)},
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )

    return token_schema.TokenSchemas(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )
