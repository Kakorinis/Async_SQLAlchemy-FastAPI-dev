from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Type

from fastapi import APIRouter
from fastapi import params

from src.schemas.dtos import BaseSchema


class BaseAbsRouter(ABC):
    """
    Базовый класс для роутеров.
    """

    def __init__(
            self,
            router_prefix: str,
            name: str,
            description: str,
            controller_dependency: params.Depends,
            short_schema_type: Type[BaseSchema],
            external_schema_type: Type[BaseSchema],
            cache_lifetime: int = 1,
            has_authentication: bool = True,
            dependencies: Optional[List[params.Depends]] = None
    ):
        self._name = name
        self._description = description
        self._has_authentication = has_authentication

        if not dependencies:
            dependencies = list()
        self._api_router = APIRouter(
            prefix=router_prefix,
            dependencies=dependencies,
        )
        self._controller_dependency = controller_dependency
        self._short_schema_type = short_schema_type
        self._external_schema_type = external_schema_type
        self._short_list_response_type = List[short_schema_type]  # type: ignore[valid-type]
        self._external_list_response_type = List[external_schema_type]  # type: ignore[valid-type]
        self._cache_lifetime = cache_lifetime

        # Добавление путей в роутер
        self.add_custom_routes()  # в кастомных могут быть пересечения с get /{id}, такой порядок их исключает
        self.add_routes()

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def has_authentication(self) -> bool:
        return self._has_authentication

    @property
    def api_router(self) -> APIRouter:
        return self._api_router

    def __str__(self) -> str:
        return f'{self._name} - {self._description}'

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def controller_dependency(self) -> params.Depends:
        return self._controller_dependency

    @property
    def short_schema_type(self) -> Type[BaseSchema]:
        return self._short_schema_type

    @property
    def external_schema_type(self) -> Type[BaseSchema]:
        return self._external_schema_type

    @property
    def short_list_response_type(
            self
    ) -> Type[List[BaseSchema]]:  # type: ignore[type-arg]
        return self._short_list_response_type

    @property
    def external_list_response_type(
            self
    ) -> Type[List[BaseSchema]]:  # type: ignore[type-arg]
        return self._external_list_response_type

    @property
    def cache_lifetime(self) -> int:
        return self._cache_lifetime

    @abstractmethod
    def add_routes(self) -> None:
        """
        Добавление обязательных админских роутов.
        """

        raise NotImplementedError

    @abstractmethod
    def add_custom_routes(self) -> None:
        """
        Добавление дополнительных роутов.
        """

        raise NotImplementedError
