import logging
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.habit import Habit
from sqlalchemy import select, Result, CursorResult, update


class CRUDHabit:
    def __init__(self):
        self.logger = logging.getLogger('database.crud.habit')

    async def get(self, title: str, user_id: int, session: AsyncSession) -> Habit:
        self.logger.debug(f"Получение привычки '{title}' для пользователя {user_id}")

        try:
            habit: Result | CursorResult = await session.execute(
                select(Habit).filter(
                    Habit.user_id == user_id,
                    Habit.title == title,
                )
            )

            result = habit.scalar_one_or_none()
            if result:
                self.logger.debug(f"Привычка '{title}' найдена (ID: {result.id})")
            else:
                self.logger.debug(f"Привычка '{title}' не найдена")
            return result

        except Exception as e:
            self.logger.error(f"Ошибка при получении привычки '{title}' для пользователя {user_id}: {str(e)}", exc_info=True)
            raise

    async def get_all(self, user_id: int, session: AsyncSession):
        self.logger.debug(f"Получение всех привычек для пользователя {user_id}")
        try:
            result = await session.execute(
                    select(
                        Habit,
                    ).filter(
                        Habit.user_id == user_id,
                    )
                )
            return result.scalars().all()
        except Exception as e:
            self.logger.error(f"Ошибка при получении всех привычек для пользователя {user_id}: {str(e)}", exc_info=True)
            raise
    async def create(self, title: str, description: str, user_id: int, session: AsyncSession) -> Habit:
        self.logger.debug(f"Создание привычки '{title}' для пользователя {user_id}")
        try:
            new_habit = Habit(
                title=title,
                description=description,
                user_id=user_id,
            )
            session.add(new_habit)
            self.logger.debug(f"Привычка '{title}' добавлена в сессию")
            return new_habit
        except Exception as e:
            self.logger.error(f"Ошибка при создании привычки '{title}' для пользователя {user_id}: {str(e)}", exc_info=True)
            raise

    async def update(self, user_id: int, title: str, data: Dict, session: AsyncSession) -> Result:
        self.logger.debug(f"Создание привычки '{title}' для пользователя {user_id}")
        try:
            habit: Result = await session.execute(
                    update(
                        Habit,
                    )
                    .where(
                        Habit.user_id == user_id,
                        Habit.title == title,
                    )
                    .values(
                        **data,
                    )
                    .returning(
                        Habit,
                    )
                )
            self.logger.debug(f"Привычка '{title}' обновлена.")
            return habit.scalar()
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении привычки '{title}' для пользователя {user_id}: {str(e)}", exc_info=True)
            raise

    async def delete(self, habit: Habit, session: AsyncSession):
        await session.delete(habit)


habit_crud: CRUDHabit = CRUDHabit()
