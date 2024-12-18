from fastapi import Depends

from src.dependencies.controller_dependencies import get_owner_controller
from src.schemas.dtos import OwnerDto
from src.schemas.dtos import OwnerFullDto
from .base_router import BaseRouter

owner_router = BaseRouter(
    router_prefix='/owner',
    name='Owner',
    description='Методы для работы с таблицей owner',
    controller_dependency=Depends(get_owner_controller),
    short_schema_type=OwnerDto,
    external_schema_type=OwnerFullDto
)
