from typing import List

from pydantic import Field

from .apartment_shema import ApartmentSchema
from .owner_dto import OwnerDto


class OwnerFullDto(OwnerDto):
    apartments: List[ApartmentSchema] = Field(
        init_var=True,
        kw_only=True,
        description='Перечень квартир в собственности',
        default_factory=list
    )
