from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import Apartment, Building
from src.models import ApartmentInfo
from src.models import Bill
from src.schemas.dtos import ApartmentDto
from src.schemas.dtos import ApartmentFullDto
from src.schemas.dtos import ApartmentInfoDto
from .base_db_repository import BaseDbRepository
from src.schemas.responses import ApartmentFullResponse


class ApartmentRepository(BaseDbRepository[Apartment, ApartmentDto, ApartmentFullDto]):
    """
    Репозиторий с типовыми дефолтными круд-методами из базового репозитория для работы с таблицами
    Apartment и ApartmentInfo.
    """
    def __init__(self, async_db_session: AsyncSession):
        super().__init__(
            async_db_session=async_db_session,
            model_type=Apartment,
            short_dto_type=ApartmentDto,
            full_dto_type=ApartmentFullDto,
            schemas_to_models_dict={
                ApartmentDto: Apartment,
                ApartmentFullDto: Apartment,
                ApartmentInfoDto: ApartmentInfo,
            },
            full_select_statement=select(Apartment).options(joinedload(Apartment.apartment_info))
        )

    async def get_apartments_full_data_with_debt(
            self,
            building_id: Optional[int] = None
    ) -> List[ApartmentFullResponse]:
        """
        Специальный метод предоставления расширенных данных о квартирах с наличием задолженности.

        :param building_id: идентификатор дома, если не передан, то поиск по всем домам.
        :return: список дто с расширенными данными о квартирах.
        """
        statement = select(self.model_type).options(
            joinedload(self.model_type.building),
            joinedload(self.model_type.owner),
            joinedload(self.model_type.bills.and_(Bill.is_paid == False))  # .and_(Bill.is_paid is False))
        ).where(self.model_type.bills.and_(Bill.is_paid == False))

        if building_id:
            statement = statement.where(self.model_type.id_building == building_id)

        models_sequence = await self.execute_select_many_statement(statement)
        return [ApartmentFullResponse.model_validate(model) for model in models_sequence]

    async def get_apartments_full_data_with_debt_by_apart_id(
            self,
            apartment_number: int,
            building_id: int
    ) -> ApartmentFullResponse:
        """
        Специальный метод предоставления расширенных данных о квартире с наличием задолженности по заранее
        известным apartment_number и building_id.

        :param apartment_number: номер квартиры.
        :param building_id: идентификатор дома.
        :return: дто с расширенными данными о квартире.
        """
        statement = select(Apartment).options(
            joinedload(Apartment.building),
            joinedload(Apartment.owner),
            joinedload(Apartment.bills.and_(Bill.is_paid == False))  # .and_(Bill.is_paid is False))
        ).where(
            and_(
                Apartment.bills.and_(Bill.is_paid == False),
                Apartment.apartment_number == apartment_number,
                Apartment.id_building == building_id
            )
        )
        model = await self.async_db_session.scalar(statement)
        return ApartmentFullResponse.model_validate(model)

    async def get_apartments_full_data_with_debt_by_project_name(
            self,
            building_project_name: Optional[str] = None
    ) -> List[ApartmentFullResponse]:
        """
        Специальный метод предоставления расширенных данных о квартирах с наличием задолженности по названию
        жилого комплекса.

        :param building_project_name: название ЖК, если не передано, то поиск по всем жилым комплексам.
        :return: список дто с расширенными данными о квартирах.
        """
        statement = select(Apartment).options(
            joinedload(Apartment.building),
            joinedload(Apartment.owner),
            joinedload(Apartment.bills.and_(Bill.is_paid == False))  # .and_(Bill.is_paid is False))
        ).where(Apartment.bills.and_(Bill.is_paid == False))

        if building_project_name:
            statement = select(Apartment).options(
                joinedload(
                    Apartment.building.and_(
                        Building.project_name == building_project_name
                    )
                ),
                joinedload(Apartment.owner),
                joinedload(Apartment.bills.and_(Bill.is_paid == False))  # .and_(Bill.is_paid is False))
            ).where(
                and_(
                    Apartment.bills.and_(Bill.is_paid == False),
                    Apartment.building.has(
                        Building.project_name == building_project_name
                                           )
                )
            )
        models_sequence = await self.execute_select_many_statement(statement)
        return [ApartmentFullResponse.model_validate(model) for model in models_sequence]
