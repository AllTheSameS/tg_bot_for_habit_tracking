from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models.user import User


async def get_user_by_tg_user_id(
        tg_user_id: int,
        session: AsyncSession,
):

    response = await session.execute(
        select(
            User
        ).filter(
            User.tg_user_id == tg_user_id
        )
    )

    return response.one_or_none()
