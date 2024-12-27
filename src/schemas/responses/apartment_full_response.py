from typing import Optional, List

from pydantic import Field

from src.schemas.dtos import ApartmentInfoDto
from src.schemas.dtos import BaseSchema
from src.schemas.dtos import BillDto
from src.schemas.dtos import BuildingDto
from src.schemas.dtos import OwnerDto


class ApartmentFullResponse(BaseSchema):
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
    apartment_info: Optional[ApartmentInfoDto] = Field(
        init_var=True,
        kw_only=True,
        description='Подробная информация о параметрах квартиры',
        default=None
    )
    building: Optional[BuildingDto] = Field(
        init_var=True,
        kw_only=True,
        description='Информация о доме квартиры',
        default=None
    )
    owner: Optional[OwnerDto] = Field(
        init_var=True,
        kw_only=True,
        description='Информация о владельце квартиры',
        default=None
    )

    bills: Optional[List[BillDto]] = Field(
        init_var=True,
        kw_only=True,
        description='Информация о квитанциях на квартиру',
        default_factory=list
    )
