from typing import Callable, AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from src.logger import AppLogger

from settings import app_settings


def get_sqlalchemy_async_session_generator(
        async_session_maker: async_sessionmaker[AsyncSession]
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    async def sqlalchemy_async_session_generator() -> AsyncGenerator[AsyncSession, None]:
        """
        Возвращает объект AsyncSession. При успешном выполнении всех запросов фиксирует изменения в БД.
        При ошибке отменяет все изменения в БД.
        В конце закрывает сессию.

        :return: AsyncSession.
        """
        AppLogger.info('Get sqlalchemy async session')

        async_session = async_session_maker()
        try:
            yield async_session

            AppLogger.info('Commit sqlalchemy async session')

            await async_session.commit()
        except Exception as exc:

            AppLogger.error(f'Exception sqlalchemy async session: {exc}')

            await async_session.rollback()
            await async_session.close()

            raise exc
        else:
            AppLogger.info('Close sqlalchemy async session')

            await async_session.close()

    return sqlalchemy_async_session_generator


# Для зависимостей подключения к БД
engine = create_async_engine(app_settings.SQL_DSN, echo=app_settings.IS_DEBUG)
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
sqlalchemy_async_session_generator = get_sqlalchemy_async_session_generator(async_session_factory)
