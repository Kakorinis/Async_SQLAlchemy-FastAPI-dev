from enum import Enum
from src.schemas.dtos import BaseSchema

from .base_response_error import BaseResponseError


class BaseResponseErrorWithData(BaseResponseError):
    """
    Базовый класс ошибок с данными.
    """

    def __init__(self, message: Enum, code: int, data: BaseSchema):
        super().__init__(message=message, code=code)
        self._data = data

    @property
    def data(self) -> BaseSchema:
        return self._data
