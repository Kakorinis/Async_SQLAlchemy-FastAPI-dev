from http import HTTPStatus

from src.enums import BaseMessageEnum
from .base_response_error import BaseResponseError


class UserNotFoundError(BaseResponseError):
    """
    Ошибка когда польователь не найден.
    """

    def __init__(self):
        super().__init__(message=BaseMessageEnum.USER_NOT_FOUND, code=HTTPStatus.BAD_REQUEST)
