from typing import Optional

from pydantic import Field

from .mixin_id_schema import MixinIdSchema


class ApartmentInfoDto(MixinIdSchema):
    room_number: int = Field(
        init_var=True,
        kw_only=True,
        description='Количество комнат'
    )

    common_square: float = Field(
        init_var=True,
        kw_only=True,
        description='Общая площадь квартиры'
    )
    kitchen_square: Optional[float] = Field(
        init_var=True,
        kw_only=True,
        description='Площадь кухни',
        default=None
    )
    balcony: Optional[bool] = Field(
        init_var=True,
        kw_only=True,
        description='Наличие балконa',
        default=None
    )
