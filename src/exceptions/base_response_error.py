from enum import Enum

from .base_error import BaseError


class BaseResponseError(BaseError):
    """
    Класс базовых ошибок ответов.
    """

    def __init__(self, message: Enum, code: int):
        super().__init__(message=message)
        self._code = code

    @property
    def code(self) -> int:
        return self._code

    def __str__(self):
        return f'{self._code} {self._message.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self._code}, {self._message.name})'
