from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import Apartment
from src.models import ApartmentInfo
from src.models import Owner
from src.schemas.dtos import ApartmentFullDto
from src.schemas.dtos import ApartmentInfoDto
from src.schemas.dtos import OwnerDto
from src.schemas.dtos import OwnerFullDto
from .base_db_repository import BaseDbRepository


class OwnerRepository(BaseDbRepository[Owner, OwnerDto, OwnerFullDto]):
    """
    Репозиторий с типовыми дефолтными круд-методами из базового репозитория для работы с таблицей Owner.
    """
    def __init__(self, async_db_session: AsyncSession):
        super().__init__(
            async_db_session=async_db_session,
            model_type=Owner,
            short_dto_type=OwnerDto,
            full_dto_type=OwnerFullDto,
            schemas_to_models_dict={
                OwnerDto: Owner,
                OwnerFullDto: Owner,
                ApartmentFullDto: Apartment,
                ApartmentInfoDto: ApartmentInfo

            },
            full_select_statement=select(Owner).options(joinedload(Owner.apartments))
        )
