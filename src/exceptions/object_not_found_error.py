from http import HTTPStatus

from src.enums import BaseMessageEnum
from .base_response_error import BaseResponseError


class ObjectNotFoundError(BaseResponseError):
    """
    Ошибка дупликации уникальных ключей.
    """

    def __init__(self):
        super().__init__(message=BaseMessageEnum.OBJECT_NOT_FOUND_ERROR_MESSAGE, code=HTTPStatus.NOT_FOUND)
