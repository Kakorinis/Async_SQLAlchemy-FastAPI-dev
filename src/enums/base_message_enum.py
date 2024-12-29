from enum import Enum


class BaseMessageEnum(Enum):
    """
    Класс базовых сообщений об ошибках.
    """

    OBJECT_NOT_FOUND_ERROR_MESSAGE = 'object_not_found_error'
    SQLALCHEMY_INTEGRITY_ERROR_MESSAGE = 'sqlalchemy_integrity_error'
    VALIDATION_ERROR_MESSAGE = 'validation_error'
    USER_NOT_FOUND = 'there is no user with such login'
