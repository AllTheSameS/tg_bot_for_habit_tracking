"""Модуль работы с токеном и паролем."""

from settings import settings
import datetime
import jwt
import bcrypt


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: datetime.timedelta | None = None,
) -> str:
    """Шифрование токена."""

    to_encode: dict = payload.copy()
    now: datetime = datetime.datetime.now(datetime.UTC)

    if expire_timedelta:
        expire: datetime = now + expire_timedelta

    else:
        expire: datetime = now + datetime.timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded: str = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """Расшифровка токена."""

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )

    return decoded


def hash_password(
    password: str,
) -> bytes:
    """Хеширование пароля."""

    salt: bytes = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    """Валидация пароля."""

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
