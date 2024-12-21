from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.common import sqlalchemy_async_session_generator
from .user_repository import UserRepository


async def get_user_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика UserRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий UserRepository.
    """
    return UserRepository(async_db_session=async_db_session)
