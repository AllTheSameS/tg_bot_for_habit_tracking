from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, CursorResult
from api.database.models.user import User


async def get_user_by_tg_user_id(
    tg_user_id: int,
    session: AsyncSession,
) -> User:
    """Функция вывода пользователя по telegram_id."""

    user: Result | CursorResult = await session.execute(
        select(User).filter(
            User.telegram_id == tg_user_id,
        )
    )

    return user.scalar_one_or_none()
