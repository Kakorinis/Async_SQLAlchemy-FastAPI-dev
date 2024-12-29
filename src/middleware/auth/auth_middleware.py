from base64 import b64decode

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.types import ASGIApp

from settings import app_settings
from .common import is_the_same_passwords
from .user_repository import UserRepository


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Класс для api и basic авторизация в сервисе.
    """
    def __init__(self, app: ASGIApp, user_repository: UserRepository):
        super().__init__(app)
        self.user_repository = user_repository


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse:  # noqa,
        # type: ignore
        """
        Проверка логина и пароля.

        :param request: Входящий запрос.
        :param call_next: Следующий в цепочке вызовов метод.
        :return: Ответ на запрос.
        """
        if request.url.path not in app_settings.PATH_NOT_REQUIRE_AUTH:

            api_key_header = request.headers.get('example_name_of_api_key')
            auth_header = request.headers.get('authorization')

            if api_key_header:
                if api_key_header == 'NEED_TO_GET_API_KEY_FROM_DB':
                    return await call_next(request)

            elif auth_header:
                scheme, credentials = auth_header.split()
                if scheme.lower() == 'basic':
                    decoded = b64decode(credentials).decode('ascii')
                    username, password = decoded.split(':')

                    user_dto = await self.user_repository.get_user_by_login(username)
                    if user_dto and user_dto.hashed_password:
                        if is_the_same_passwords(password, user_dto.hashed_password):
                            return await call_next(request)

            content = {'detail': 'Authorization error'}
            response = JSONResponse(content=content, status_code=HTTP_401_UNAUTHORIZED)
            response.headers['WWW-Authenticate'] = 'Basic'  # оставлено для сваггера
            return response
        return await call_next(request)
