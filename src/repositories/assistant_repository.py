from sqlalchemy.ext.asyncio import AsyncSession


class AssistantRepository:
    """
    Репозиторий для специальных не базовых методов.
    """
    def __init__(self, async_db_session: AsyncSession):
        self.async_db_session = async_db_session

    # TODO можно реализовать какие-нибудь специфичные запросы в БД
