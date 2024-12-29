from traceback import format_exc

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from src.logger import AppLogger
from src.exceptions import BaseResponseError
from src.exceptions import BaseResponseErrorWithData


class JsonResponseMapper:
    """
    Сборка JSON ответа.
    """

    @staticmethod
    async def get_from_base_response_error(exception: BaseResponseError, message: str) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для базового исключения.

        :param exception: Объект базового исключения.
        :param message: Сообщение ошибки.
        :return: JSON ответ с сообщением об ошибке.
        """
        AppLogger.error(f'Mapping http error json response: {exception}')

        return JSONResponse(
            status_code=exception.code,
            content={
                'message': message,
            }
        )

    @staticmethod
    async def get_from_base_response_error_with_data(
            exception: BaseResponseErrorWithData,
            message: str
    ) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для исключения с данными.

        :param exception: Объект исключения с данными.
        :param message: Сообщение ошибки.
        :return: JSON ответ с сообщением об ошибке.
        """
        AppLogger.error(f'Mapping http error json response: {exception}')

        generated_message: str
        try:
            generated_message = message.format(**exception.data.model_dump())
        except KeyError as exc:
            AppLogger.error(f'Error formatting message {message}: {exc}')

            generated_message = message
        content = {
            'message': generated_message,
        }
        content.update(exception.data.model_dump())

        return JSONResponse(status_code=exception.code, content=content)

    @staticmethod
    async def get_from_pydantic_validation_error(pydantic_validation_error: PydanticValidationError) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для Pydantic исключения.

        :param pydantic_validation_error: Объект исключения.
        :return: JSON ответ с сообщением об ошибке.
        """
        AppLogger.error(f'Mapping validation error json response: {pydantic_validation_error}')

        validation_errors_list = list()
        default_description = pydantic_validation_error.__str__().split('For further')
        if len(default_description) <= 1:
            default_description = None
        else:
            default_description = default_description[0].replace('\n', '.')

        for detail_item in pydantic_validation_error.errors():
            validation_errors_list.append(
                {
                    'location': detail_item.get('loc'),
                    'message': detail_item.get('msg'),
                    'type': detail_item.get('type'),
                }
            )
        if len(validation_errors_list) == 1:
            validation_errors_list[0]['message'] = default_description

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=validation_errors_list
        )

    @staticmethod
    async def get_from_exception(exception: Exception) -> JSONResponse:
        """
        Возвращает JSON ответ с сообщением об ошибке для внештатного исключения.

        :param exception: Объект исключения.
        :return: JSON ответ с сообщением об ошибке.
        """
        AppLogger.error(f'Mapping unexpected error json response: {exception}')

        exception_traceback = format_exc(limit=1).replace('\\n', '')

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': f'{exception.__class__.__name__}: {exception} {exception_traceback}',
            }
        )
