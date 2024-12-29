from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from fastapi import Path
from fastapi import Request
from fastapi import params
from fastapi import status
from fastapi_cache.decorator import cache

from src.controllers import BaseController
from src.enums import BaseMessageEnum
from src.logger import AppLogger
from src.schemas.dtos import BaseSchema
from .base_abs_router import BaseAbsRouter


class BaseRouter(BaseAbsRouter):
    """
    Роутер для админ-панели.
    """

    def __init__(
            self,
            router_prefix: str,
            name: str,
            description: str,
            controller_dependency: params.Depends,
            short_schema_type: Type[BaseSchema],
            external_schema_type: Type[BaseSchema],
            cache_lifetime: int = 60,
            has_authentication: bool = True,
            dependencies: Optional[List[params.Depends]] = None
    ):
        super().__init__(
            router_prefix=router_prefix,
            name=name,
            description=description,
            controller_dependency=controller_dependency,
            short_schema_type=short_schema_type,
            external_schema_type=external_schema_type,
            cache_lifetime=cache_lifetime,
            has_authentication=has_authentication,
            dependencies=dependencies
        )

    def add_routes(self):
        AppLogger.debug(f'Add routes for admin router: {self.name}')

        external_schema_type = self.external_schema_type
        short_list_response_type = self.short_list_response_type
        external_list_response_type = self.external_list_response_type
        controller_dependency = self.controller_dependency

        object_id_path = Path(alias='id', title='Идентификатор объекта', ge=1, examples=[1])

        @self.api_router.put(
            path='',
            summary='Создание/обновление объекта',
            response_model=self.external_schema_type,
            status_code=status.HTTP_200_OK
        )
        async def upsert(
                external_dto: external_schema_type,  # type: ignore[valid-type]
                controller: BaseController = controller_dependency  # type: ignore
        ) -> external_schema_type:  # type: ignore[valid-type]
            """
            Создание/обновление объекта в БД.
            """

            return await controller.upsert(  # type: ignore[no-any-return]
                external_schema=external_dto
            )

        @self.api_router.put(
            path='/many',
            summary='Создание/обновление списка объектов',
            response_model=self.short_list_response_type,
            status_code=status.HTTP_200_OK
        )
        async def upsert_many(
                external_dto_list: List[external_schema_type],  # type: ignore[valid-type]
                controller: BaseController = controller_dependency  # type: ignore
        ) -> external_list_response_type:  # type: ignore[valid-type]
            """
            Создание/обновление списка объектов в БД.
            """

            return await controller.upsert_many(external_schemas_list=external_dto_list)

        @self.api_router.get(
            path='/all_full',
            summary='Получение списка полных объектов',
            response_model=self.external_list_response_type,
            status_code=status.HTTP_200_OK
        )
        @cache(expire=self.cache_lifetime)
        async def get_all_full(
                _: Request,  # Необходимо из-за специфики работы fastapi_cache
                controller: BaseController = controller_dependency  # type: ignore
        ) -> external_list_response_type:  # type: ignore[valid-type]
            """
            Выборка полных DTO объектов из БД.
            """

            return await controller.get_all_full()

        @self.api_router.get(
            path='/all_short',
            summary='Получение списка кратких объектов',
            response_model=self.short_list_response_type,
            status_code=status.HTTP_200_OK
        )
        @cache(expire=self.cache_lifetime)
        async def get_all_short(
                _: Request,  # Необходимо из-за специфики работы fastapi_cache
                controller: BaseController = controller_dependency  # type: ignore
        ) -> short_list_response_type:  # type: ignore[valid-type]
            """
            Выборка кратких DTO объектов из БД.
            """

            return await controller.get_all_short()

        @self.api_router.get(
            path='/{id}',
            summary='Получение объекта по ID',
            response_model=self.external_schema_type,
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    'description': 'Успешное получение объекта',
                    'model': external_schema_type,
                },
                status.HTTP_404_NOT_FOUND: {
                    'description': 'Объект не найден',
                    'content': {
                        'application/json': {
                            'example': {
                                'message': BaseMessageEnum.OBJECT_NOT_FOUND_ERROR_MESSAGE.value,
                            },
                        },
                    },
                },
            }
        )
        @cache(expire=self.cache_lifetime)
        async def get_one_by_id(
                _: Request,  # Необходимо из-за специфики работы fastapi_cache
                object_id: int = object_id_path,
                controller: BaseController = controller_dependency  # type: ignore
        ) -> external_schema_type:  # type: ignore[valid-type]
            """
            Выборка одного DTO объекта из БД через метод сессии.
            """

            return await controller.get_one_by_id(  # type: ignore[no-any-return]
                object_id=object_id
            )

        @self.api_router.delete(
            path='/many',
            summary='Удаление нескольких объектов по ID',
            response_model=Dict,
            status_code=status.HTTP_200_OK
        )
        async def delete_many(
                objects_ids_list: List[int],
                controller: BaseController = controller_dependency  # type: ignore
        ) -> Dict:  # type: ignore[type-arg]
            """
            Удаление нескольких объектов из БД.
            """

            return await controller.delete_many(objects_ids_list=objects_ids_list)

        @self.api_router.delete(
            path='/{id}',
            summary='Удаление объекта по ID',
            response_model=Dict,
            status_code=status.HTTP_200_OK
        )
        async def delete(
                object_id: int = object_id_path,
                controller: BaseController = controller_dependency  # type: ignore
        ) -> Dict:  # type: ignore[type-arg]
            """
            Удаление объекта из БД.
            """

            return await controller.delete(object_id=object_id)

    def add_custom_routes(self) -> None:
        """
        Дополнительные маршруты не требуются.
        """
        pass
