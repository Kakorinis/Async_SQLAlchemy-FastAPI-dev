from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Users
from .user_dto import UserDto


class UserRepository:
    """
    Репозиторий для проверки прав пользователей.
    """
    def __init__(self, async_db_session: AsyncSession):
        self.async_db_session = async_db_session

    async def get_user_by_login(self, login: str) -> UserDto:
        stmt = select(Users).where(Users.login == login)
        model = await self.async_db_session.scalar(stmt)
        return UserDto.model_validate(model)
