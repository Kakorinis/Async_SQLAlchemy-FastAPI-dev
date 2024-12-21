from fastapi import Depends

from src.dependencies.controller_dependencies import get_building_controller
from src.schemas.dtos import BuildingDto
from .base_router import BaseRouter

building_router = BaseRouter(
    router_prefix='/building',
    name='Building',
    description='Методы для работы с таблицей building',
    controller_dependency=Depends(get_building_controller),
    short_schema_type=BuildingDto,
    external_schema_type=BuildingDto,
    has_authentication=True
)
