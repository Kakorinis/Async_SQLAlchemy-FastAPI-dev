from abc import ABC
from typing import Generic
from typing import List
from typing import Type
from typing import TypeVar

from src.exceptions import ObjectNotFoundError
from src.logger import AppLogger
from src.repositories.base_db_repository import BaseDbRepository
from src.schemas.dtos import BaseSchema

MainRepositoryType = TypeVar('MainRepositoryType', bound=BaseDbRepository)  # type: ignore[type-arg]
ShortSchema = TypeVar('ShortSchema', bound=BaseSchema)
FullSchema = TypeVar('FullSchema', bound=BaseSchema)
ExternalSchema = TypeVar('ExternalSchema', bound=BaseSchema)


class BaseControllerInterface:
    """
    Базовый интерфейс контроллера.
    """
    pass


class BaseController(
    BaseControllerInterface,
    Generic[MainRepositoryType, ShortSchema, FullSchema, ExternalSchema],
    ABC
):

    def __init__(
            self,
            main_repository: MainRepositoryType,
            short_schema_type: Type[ShortSchema],
            full_schema_type: Type[FullSchema],
            external_schema_type: Type[ExternalSchema]
    ):
        self._main_repository = main_repository
        self._short_schema_type = short_schema_type
        self._full_schema_type = full_schema_type
        self._external_schema_type = external_schema_type
        self._short_list_response_type = List[short_schema_type]  # type: ignore[valid-type]
        self._external_list_response = List[external_schema_type]  # type: ignore[valid-type]

    @property
    def main_repository(self) -> MainRepositoryType:
        return self._main_repository

    @property
    def short_schema_type(self) -> Type[ShortSchema]:
        return self._short_schema_type

    @property
    def full_schema_type(self) -> Type[FullSchema]:
        return self._full_schema_type

    @property
    def external_schema_type(self) -> Type[ExternalSchema]:
        return self._external_schema_type

    @property
    def short_list_response_type(self) -> Type[List[ShortSchema]]:
        return self._short_list_response_type

    @property
    def external_list_response(self) -> Type[List[ExternalSchema]]:
        return self._external_list_response

    async def map_full_from_external(self, external_schema: ExternalSchema) -> FullSchema:
        """
        Сборка полной внутренней схемы из внешней.
        Для уникальных случаев использования метод необходимо перегружать.

        :param external_schema: Экземпляр внешней схемы.
        :return: Экземпляр полной внутренней схемы.
        """
        AppLogger.info(f'Map full schema from external schema: {external_schema}')

        return self._full_schema_type(**external_schema.model_dump())

    async def map_external_from_full(self, full_schema: FullSchema) -> ExternalSchema:
        """
        Сборка внешней схемы из полной внутренней.
        Для уникальных случаев использования метод необходимо перегружать.

        :param full_schema: Экземпляр полной внутренней схемы.
        :return: Экземпляр внешней схемы.
        """
        AppLogger.info(f'Map external schema from full schema: {full_schema}')

        return self._external_schema_type(**full_schema.model_dump())

    async def map_full_list_from_external_list(self, external_schemas_list: List[ExternalSchema]) -> List[FullSchema]:
        """
        Сборка списка полных внутренних схем из списка внешних.
        Для уникальных случаев использования метод необходимо перегружать.

        :param external_schemas_list: Список экземпляров внешних схем.
        :return: Список экземпляров полных внутренних схем.
        """
        AppLogger.info(f'Map full schemas list from external schemas list: {external_schemas_list}')

        return [self._full_schema_type(**external_schema.model_dump()) for external_schema in external_schemas_list]

    async def map_external_list_from_full_list(
            self,
            full_schemas_list: List[FullSchema]
    ) -> List[ExternalSchema]:
        """
        Сборка списка внешних схем из списка полных внутренних.
        Для уникальных случаев использования метод необходимо перегружать.

        :param full_schemas_list: Список экземпляров полных внутренних схем.
        :return: Список экземпляров внешних схем.
        """
        AppLogger.info(f'Map external schemas list from full internal schemas list: {full_schemas_list}')

        return [self._external_schema_type(**full_schema.model_dump()) for full_schema in full_schemas_list]

    async def map_short_list_from_full_list(
            self,
            full_schemas_list: List[FullSchema]
    ) -> List[ShortSchema]:
        """
        Сборка списка кратких схем из списка полных внутренних.
        Для уникальных случаев использования метод необходимо перегружать.

        :param full_schemas_list: Список экземпляров полных внутренних схем.
        :return: Список экземпляров кратких схем.
        """
        AppLogger.info(f'Map short schemas list from full internal schemas list: {full_schemas_list}')

        return [
            self._short_schema_type(**full_schema.model_dump())
            for full_schema in full_schemas_list
        ]

    async def upsert(self, external_schema: ExternalSchema) -> ExternalSchema:
        """
        Создание/обновление объекта в БД.

        :param external_schema: DTO для создания/обновления объекта.
        :return: DTO с обновленными данными.
        """
        AppLogger.info(f'Upsert: {external_schema}')

        return await self.map_external_from_full(
            full_schema=await self.main_repository.upsert(
                dto=await self.map_full_from_external(external_schema=external_schema)
            )
        )

    async def upsert_many(self, external_schemas_list: List[ExternalSchema]) -> List[ExternalSchema]:
        """
        Создание/обновление списка объектов в БД.

        :param external_schemas_list: Список DTO для создания/обновления объектов.
        :return: Список DTO с обновленными данными.
        """
        AppLogger.info(f'Upsert many: {external_schemas_list}')

        return await self.map_external_list_from_full_list(  # type: ignore[arg-type]
            full_schemas_list=await self.main_repository.upsert_many(
                dto_list=await self.map_full_list_from_external_list(
                    external_schemas_list=external_schemas_list
                )
            )
        )

    async def get_one_by_id(self, object_id: int) -> ExternalSchema:
        """
        Выборка одного DTO объекта из БД через метод сессии.

        :param object_id: ID объекта.
        :return: DTO объекта.
        """
        AppLogger.info(f'Get one object: {object_id}')

        full_schema = await self.main_repository.get_one_full_by_id(object_id=object_id)
        if full_schema:
            return await self.map_external_from_full(full_schema=full_schema)

        raise ObjectNotFoundError()

    async def select_one_by_id(self, object_id: int) -> ExternalSchema:
        """
        Выборка одного DTO объекта из БД через SELECT.

        :param object_id: ID объекта.
        :return: DTO объекта.
        """
        AppLogger.info(f'Select one object: {object_id}')

        full_schema = await self.main_repository.select_one_full_by_id(object_id=object_id)
        if full_schema:
            return await self.map_external_from_full(full_schema=full_schema)

        raise ObjectNotFoundError()

    async def get_all_short(self) -> List[ShortSchema]:
        """
        Выборка всех DTO объектов из БД через SELECT.

        :return: Список кратких DTO объектов.
        """
        AppLogger.info('Select all objects')
        models_dtos = await self.main_repository.select_all_short()
        return await self.map_short_list_from_full_list(models_dtos)

    async def get_all_full(self) -> List[ExternalSchema]:
        """
        Выборка всех DTO объектов из БД через SELECT.

        :return: Список DTO объектов.
        """
        AppLogger.info('Select all objects')
        models_dtos = await self.main_repository.select_all_full()

        return await self.map_external_list_from_full_list(models_dtos)

    async def delete(
            self,
            object_id: int
    ) -> dict:  # type: ignore[type-arg]
        """
        Удаление объекта из БД.

        :param object_id: ID объекта.
        :return: Статус удаления.
        """
        # TODO: потом решить как возвращать статус удаления в админке
        AppLogger.info(f'Delete object: {object_id}')

        await self.main_repository.delete(object_id=object_id)

        return dict()

    async def delete_many(
            self,
            objects_ids_list: List[int]
    ) -> dict:  # type: ignore[type-arg]
        """
        Удаление нескольких объектов из БД.

        :param objects_ids_list: Список ID объектов.
        :return: Статус удаления.
        """
        # TODO: потом решить как возвращать статус удаления в админке
        AppLogger.info(f'Delete many objects: {objects_ids_list}')

        await self.main_repository.delete_many(objects_ids_list=objects_ids_list)

        return dict()
