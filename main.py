from fastapi import FastAPI
from uvicorn import run

from settings import app_settings
from src.logger import AppLogger
from src.routers import apartment_router
from src.routers import assistant_router
from src.routers import bill_router
from src.routers import building_router
from src.routers import owner_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis


app = FastAPI(
    title=app_settings.SWAGGER_TITLE,
    version=app_settings.APP_VERSION
)

# Настройки Redis
redis_client = Redis(host='localhost', port=6379, db=0)

# Инициализация кеша
FastAPICache.init(RedisBackend(redis_client))

app.include_router(
    apartment_router.api_router,
    tags=[apartment_router.name]
)
app.include_router(
    owner_router.api_router,
    tags=[owner_router.name]
)
app.include_router(
    bill_router.api_router,
    tags=[bill_router.name]
)
app.include_router(
    building_router.api_router,
    tags=[building_router.name]
)

app.include_router(
    assistant_router.api_router,
    tags=[assistant_router.name]
)

AppLogger.init(is_debug=app_settings.IS_DEBUG)


def main() -> None:
    """
    Запуск тестового сервера.
    """
    try:
        AppLogger.info('Start FastAPI application')
        run(app, host=app_settings.HOST, port=app_settings.PORT, log_config=AppLogger.LOGGING_CONFIG)  # reload=True,
    except Exception as e:
        pass
        AppLogger.error(f'❌ FastAPI start filed: {e}')


if __name__ == '__main__':
    main()