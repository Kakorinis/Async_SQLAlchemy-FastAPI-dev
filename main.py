from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import run
from pydantic import ValidationError as PydanticValidationError
from settings import app_settings
from src.dependencies.common import sqlalchemy_async_session_generator
from src.exceptions import BaseResponseError
from src.logger import AppLogger
from src.middleware.auth import AuthMiddleware
from src.middleware.auth import get_user_repository
from src.routers import apartment_router
from src.routers import assistant_router
from src.routers import bill_router
from src.routers import building_router
from src.routers import owner_router
from src.utils.json_response_mapper import JsonResponseMapper

app = FastAPI(
    title=app_settings.SWAGGER_TITLE,
    version=app_settings.APP_VERSION
)


@app.exception_handler(BaseResponseError)
async def handle_base_response_error(_: Request, exception: BaseResponseError) -> JSONResponse:
    """
    Обработка ошибок без данных.

    :param _: Запрос.
    :param exception: Объект исключения без данных.
    :return: Ответ с сообщением об ошибке.
    """
    message = exception.message.value
    return await JsonResponseMapper.get_from_base_response_error(exception=exception, message=message)


@app.exception_handler(PydanticValidationError)
async def handle_validation_error(_: Request, exception: PydanticValidationError) -> JSONResponse:
    """
    Обработка ошибок валидации Pydantic.

    :param _: Внешний запрос.
    :param exception: Объект исключения валидации Pydantic.
    :return: Ответ с сообщением об ошибке.
    """
    return await JsonResponseMapper.get_from_pydantic_validation_error(pydantic_validation_error=exception)


@app.exception_handler(Exception)
async def handle_exception(_: Request, exception: Exception) -> JSONResponse:
    """
    Обработка внештатных исключений.

    :param _: Запрос.
    :param exception: Объект исключения.
    :return: Ответ с сообщением об ошибке.
    """
    return await JsonResponseMapper.get_from_exception(exception=exception)

# Настройки Redis
redis_client = Redis(host='localhost', port=6379, db=0)

# Инициализация кеша
FastAPICache.init(RedisBackend(redis_client), expire=60)

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
    # dependencies=assistant_router.dependencies
)


AppLogger.init(is_debug=app_settings.IS_DEBUG)

@app.middleware("http")
async def auth_middleware(request, call_next):
    async for session in sqlalchemy_async_session_generator():
        user_repository = await get_user_repository(session)
        middleware = AuthMiddleware(app, user_repository=user_repository)
        response = await middleware.dispatch(request, call_next)
        return response


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
