from typing import List

from src.logger import AppLogger
from src.repositories import OwnerRepository
from src.schemas.dtos import OwnerDto
from src.schemas.dtos import OwnerFullDto
from .base_controller import BaseController


class OwnerController(
    BaseController[
        OwnerRepository,
        OwnerDto,
        OwnerFullDto,
        OwnerFullDto,
    ]
):
    def __init__(self, main_repository: OwnerRepository):
        super().__init__(
            main_repository=main_repository,
            short_schema_type=OwnerDto,
            full_schema_type=OwnerFullDto,
            external_schema_type=OwnerDto,
        )

    async def map_full_from_external(self, external_schema: OwnerFullDto) -> OwnerDto:
        """
        Сборка полной внутренней схемы из внешней.
        Метод переопределен,т.к. в БД пишется фул схема, а для овнеров решено писать короткую, которая и яв-ся внешней.

        :param external_schema: Экземпляр внешней схемы.
        :return: Экземпляр полной внутренней схемы.
        """
        return OwnerDto.model_validate(external_schema)

    async def map_external_from_full(self, full_schema: OwnerFullDto) -> OwnerFullDto:
        """
        Сборка внешней схемы из полной внутренней.
        Метод переопределен.

        :param full_schema: Экземпляр полной внутренней схемы.
        :return: Экземпляр полной внутренней схемы.
        """
        return full_schema

    async def map_full_list_from_external_list(self, external_schemas_list: List[OwnerFullDto]) -> List[OwnerDto]:
        """
        Сборка списка полных внутренних схем из списка внешних.
        Метод переопределен, используетя при множественном создании/апдейте, там короткие схемы.

        :param external_schemas_list: Список экземпляров внешних схем.
        :return: Список экземпляров полных внутренних схем.
        """
        AppLogger.info(f'Map full schemas list from external schemas list: {external_schemas_list}')

        return [OwnerDto.model_validate(dto) for dto in external_schemas_list]

    async def map_external_list_from_full_list(
            self,
            full_schemas_list: List[OwnerFullDto]
    ) -> List[OwnerFullDto]:
        """
        Сборка списка внешних схем из списка полных внутренних.
        Метод переопределен.

        :param full_schemas_list: Список экземпляров полных внутренних схем.
        :return: Список экземпляров полных внутренних схем.
        """
        AppLogger.info(f'Map external schemas list from full internal schemas list: {full_schemas_list}')

        return full_schemas_list
