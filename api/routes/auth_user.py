from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, status
from jwt import InvalidTokenError
from api.schemas import user_schema
from api.schemas import token_schemas
from fastapi.exceptions import HTTPException
from api.auth.utils import validate_password, encode_jwt, decode_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_async_session
from sqlalchemy import select
from api.database.models.user import User

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:

    try:

        payload = decode_jwt(
            token=token,
        )

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}",
        )

    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(get_async_session)
) -> user_schema.UserSchema:

    user = await session.execute(
        select(
            User
        ).filter(
            User.telegram_id == payload.get("sub")
        )
    )

    if user := user.one_or_none()[0]:
        return user_schema.UserSchema(
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
    user: user_schema.UserSchema = Depends(get_current_auth_user),
):

    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def validate_auth_user(
        user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await session.execute(
        select(
            User
        ).filter(
            User.telegram_id == int(user_form.username)
        )
    )

    if not (user := user.one_or_none()[0]):
        raise unauthed_exc

    if not validate_password(
        password=user_form.password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


@auth_router.post("/login", response_model=token_schemas.TokenSchemas)
async def auth_user_issue_jwt(
        user: user_schema.UserSchema = Depends(validate_auth_user),
):
    """Cоздание JWT токена."""

    payload = {
        "sub": user.telegram_id,
        "name": user.name,
        "surname": user.surname,
    }

    token = encode_jwt(payload=payload)

    return token_schemas.TokenSchemas(
        access_token=token,
        token_type="Bearer",
    )
