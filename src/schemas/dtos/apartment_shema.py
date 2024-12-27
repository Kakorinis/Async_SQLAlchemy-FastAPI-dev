from pydantic import Field
from pydantic import field_validator

from .base_schema import BaseSchema


class ApartmentSchema(BaseSchema):

    utility_account: str = Field(
        init_var=True,
        kw_only=True,
        max_length=100,
        description='Лицевой счет'
    )
    apartment_number: int = Field(
        init_var=True,
        kw_only=True,
        description='Номер квартиры'
    )

    floor: int = Field(
        init_var=True,
        kw_only=True,
        description='Этаж'
    )

    @field_validator('utility_account', mode='before')
    @classmethod
    def convert_value_to_str(cls, data: str | int) -> str:
        if isinstance(data, int):
            return str(data)
        return data
