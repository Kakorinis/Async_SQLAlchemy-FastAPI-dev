from typing import List

from src.logger import AppLogger
from src.repositories import BuildingRepository
from src.schemas.dtos import BuildingDto
from src.schemas.dtos import BuildingFullDto
from .base_controller import BaseController


class BuildingController(
    BaseController[
        BuildingRepository,
        BuildingDto,
        BuildingFullDto,
        BuildingDto,
    ]
):
    def __init__(self, main_repository: BuildingRepository):
        super().__init__(
            main_repository=main_repository,
            short_schema_type=BuildingDto,
            full_schema_type=BuildingFullDto,
            external_schema_type=BuildingDto,
        )

    async def get_all_full(self) -> List[BuildingFullDto]:
        """
        Выборка всех DTO объектов из БД через SELECT.
        Метод переопределен, т.к. внешняя схема отличается от полной схемы, а вернуть нужно полную.

        :return: Список DTO объектов.
        """
        AppLogger.info('Select all objects')
        models_sequence = await self.main_repository.select_all_full()

        return [self._full_schema_type.model_validate(model) for model in models_sequence]
