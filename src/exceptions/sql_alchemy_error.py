from http import HTTPStatus

from src.enums import BaseMessageEnum
from .base_response_error import BaseResponseError


class SqlAlchemyError(BaseResponseError):
    """
    Ошибка дупликации уникальных ключей.
    """

    def __init__(self):
        super().__init__(message=BaseMessageEnum.SQLALCHEMY_INTEGRITY_ERROR_MESSAGE, code=HTTPStatus.BAD_REQUEST)
