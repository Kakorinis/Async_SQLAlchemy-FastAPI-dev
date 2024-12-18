from fastapi import Depends

from src.dependencies.controller_dependencies import get_bill_controller
from src.schemas.dtos import BillDto
from .base_router import BaseRouter

bill_router = BaseRouter(
    router_prefix='/bill',
    name='Bill',
    description='Методы для работы с таблицей bill',
    controller_dependency=Depends(get_bill_controller),
    short_schema_type=BillDto,
    external_schema_type=BillDto
)
