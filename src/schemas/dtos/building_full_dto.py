from typing import List

from pydantic import Field

from .apartment_full_dto import ApartmentFullDto
from .building_dto import BuildingDto


class BuildingFullDto(BuildingDto):

    apartments: List[ApartmentFullDto] = Field(
        init_var=True,
        kw_only=True,
        description='Список квартир дома',
        default_factory=list
    )
