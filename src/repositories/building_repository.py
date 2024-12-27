from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import Apartment
from src.models import Building
from src.schemas.dtos import ApartmentFullDto
from src.schemas.dtos import BuildingDto
from src.schemas.dtos import BuildingFullDto
from .base_db_repository import BaseDbRepository


class BuildingRepository(BaseDbRepository[Building, BuildingDto, BuildingFullDto]):
    """
    Репозиторий с типовыми дефолтными круд-методами из базового репозитория для работы с таблицей Building.
    """
    def __init__(self, async_db_session: AsyncSession):
        super().__init__(
            async_db_session=async_db_session,
            model_type=Building,
            short_dto_type=BuildingDto,
            full_dto_type=BuildingFullDto,
            schemas_to_models_dict={
                BuildingDto: Building,
                BuildingFullDto: Building,
                ApartmentFullDto: Apartment,
            },
            full_select_statement=select(Building).options(
                joinedload(Building.apartments).joinedload(Apartment.apartment_info)
            )
        )
