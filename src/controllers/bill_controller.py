from src.repositories import BillRepository
from src.schemas.dtos import BillDto
from .base_controller import BaseController


class BillController(
    BaseController[
        BillRepository,
        BillDto,
        BillDto,
        BillDto,
    ]
):
    def __init__(self, main_repository: BillRepository):
        super().__init__(
            main_repository=main_repository,
            short_schema_type=BillDto,
            full_schema_type=BillDto,
            external_schema_type=BillDto,
        )
