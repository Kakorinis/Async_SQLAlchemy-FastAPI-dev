from typing import List, Optional

from src.repositories import ApartmentRepository
from src.schemas.dtos import ApartmentDto
from src.schemas.dtos import ApartmentFullDto
from .base_controller import BaseController
from src.schemas.responses import ApartmentFullResponse


class ApartmentController(
    BaseController[
        ApartmentRepository,
        ApartmentDto,
        ApartmentFullDto,
        ApartmentFullDto,
    ]
):
    def __init__(self, main_repository: ApartmentRepository):
        super().__init__(
            main_repository=main_repository,
            short_schema_type=ApartmentDto,
            full_schema_type=ApartmentFullDto,
            external_schema_type=ApartmentFullDto,
        )

    async def get_apartments_full_data_with_debt(
            self,
            building_id: Optional[int] = None
    ) -> List[ApartmentFullResponse]:
        """
        Получение списка расширенных данных о квартирах с задолженностью.

        :param building_id: иденификатор дома. Его может не быть, тогда поиск среди всех домов.
        :return: список дто ApartmentFullResponse
        """
        return await self.main_repository.get_apartments_full_data_with_debt(building_id)

    async def get_apartments_full_data_with_debt_by_apart_id(
            self,
            apartment_number: int,
            building_id: int
    ) -> ApartmentFullResponse:
        """
        Получение расширенных данных о квартире с задолженностью с заранее известными apartment_number и building_id.

        :param apartment_number: номер квартиры.
        :param building_id: иденификатор дома.
        :return: дто ApartmentFullResponse
        """
        return await self.main_repository.get_apartments_full_data_with_debt_by_apart_id(apartment_number, building_id)

    async def get_apartments_full_data_with_debt_by_project_name(
            self,
            building_project_name: Optional[str] = None
    ) -> List[ApartmentFullResponse]:
        """
        Получение списка расширенных данных о квартирах с задолженностью по названию ЖК.

        :param building_project_name: название жилого комплекса. Его может не быть, тогда поиск среди всех ЖК.
        :return: список дто ApartmentFullResponse
        """
        return await self.main_repository.get_apartments_full_data_with_debt_by_project_name(building_project_name)
