from enum import Enum


class BaseError(Exception):
    """
    Базовый класс ошибок.
    """

    def __init__(self, message: Enum):
        self._message = message

    @property
    def message(self) -> Enum:
        return self._message

    def __str__(self):
        return self._message.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self._message.name})'
