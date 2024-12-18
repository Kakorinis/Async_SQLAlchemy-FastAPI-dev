from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Bill
from src.schemas.dtos import BillDto
from .base_db_repository import BaseDbRepository


class BillRepository(BaseDbRepository[Bill, BillDto, BillDto]):
    """
    Репозиторий с типовыми дефолтными круд-методами из базового репозитория для работы с таблицей Bill.
    """
    def __init__(self, async_db_session: AsyncSession):
        super().__init__(
            async_db_session=async_db_session,
            model_type=Bill,
            short_dto_type=BillDto,
            full_dto_type=BillDto
        )
