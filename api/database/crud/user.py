from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class CRUDUser:

    async def get_user(self, user_id: int, session: AsyncSession) -> User | None:
        response: User = await session.execute(
            select(User).filter(User.telegram_id == user_id)
            .options(selectinload(User.habits)))
        return response.scalar_one_or_none()

    async def create(self, data: dict, session: AsyncSession) -> User | None:
        new_user: User = User(
            **data,
        )
        session.add(new_user)
        await session.commit()
        return new_user


    async def update_user(self, user_id: int, session: AsyncSession) -> Optional[Dict]:
        pass



user_crud: CRUDUser = CRUDUser()