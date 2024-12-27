from pydantic import Field
from pydantic import field_validator

from src.enums import BaseMessageEnum
from src.exceptions.base_response_with_data import BaseResponseErrorWithData
from .error_schema import ErrorSchema
from .mixin_id_schema import MixinIdSchema


class OwnerDto(MixinIdSchema):
    fullname: str = Field(
        init_var=True,
        kw_only=True,
        description='ФИО владельца'
    )

    passport_series: str = Field(
        init_var=True,
        kw_only=True,
        description='Серия паспорта'
    )
    passport_values: str = Field(
        init_var=True,
        kw_only=True,
        description='Номер паспорта'
    )
    phone: str = Field(
        init_var=True,
        kw_only=True,
        description='Сотовый телефон'
    )

    @field_validator('fullname', mode='before')
    @classmethod
    def get_fullname_validation(cls, data: str | int) -> str:
        fullname_list = data.split(' ')
        fullname_list = [word for word in fullname_list if len(word) > 0]  # исключение лишних пробелов
        fullname_list = [word.title() for word in fullname_list]  # стандартизация
        fixed_fullname = ' '.join(fullname_list)
        if any(symbol.isdigit() or symbol.isascii() for symbol in fixed_fullname.replace(' ', '')):
            raise BaseResponseErrorWithData(
                message=BaseMessageEnum.VALIDATION_ERROR_MESSAGE,
                code=422,
                data=ErrorSchema(
                    wrong_data_key='fullname',
                    data=data,
                    reason='ФИО содержит латинскую букву либо цифру'
                )
            )
        return fixed_fullname

    @field_validator('passport_series', mode='before')
    @classmethod
    def get_series_validation(cls, data: str) -> str:
        fixed_data = ''.join([el for el in data if el.isdigit()])
        if len(fixed_data) != 4:
            raise BaseResponseErrorWithData(
                message=BaseMessageEnum.VALIDATION_ERROR_MESSAGE,
                code=422,
                data=ErrorSchema(
                    wrong_data_key='passport_series',
                    data=data,
                    reason='В серии паспорта должно быть 4 цифры'
                )
            )
        return fixed_data

    @field_validator('passport_values', mode='before')
    @classmethod
    def get_passport_number_validation(cls, data: str) -> str:
        fixed_data = ''.join([el for el in data if el.isdigit()])
        if len(fixed_data) != 6:
            raise BaseResponseErrorWithData(
                message=BaseMessageEnum.VALIDATION_ERROR_MESSAGE,
                code=422,
                data=ErrorSchema(
                    wrong_data_key='passport_values',
                    data=data,
                    reason='В номере паспорта должно быть 6 цифр'
                )
            )
        return fixed_data

    @field_validator('phone', mode='before')
    @classmethod
    def get_phone_validation(cls, data: str) -> str:
        fixed_data = ''.join([el for el in data if el.isdigit()])
        if len(fixed_data) != 11:
            raise BaseResponseErrorWithData(
                message=BaseMessageEnum.VALIDATION_ERROR_MESSAGE,
                code=422,
                data=ErrorSchema(
                    wrong_data_key='phone',
                    data=data,
                    reason='В номере телефона должно быть 11 цифр'
                )
            )
        if fixed_data.startswith('7'):  # стандартизаия
            fixed_data = f'8{fixed_data[1:]}'
        return fixed_data
