from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends


class UniqueRouter:
    """
    Кастомизированный HTTP API роутер, в котором нужны уникальные методы, а не типовые.
    """

    def __init__(
            self,
            router_prefix: str,
            name: str,
            description: str,
            has_authentication: bool = True,
            dependencies: Optional[List[Depends]] = None
    ):
        """
        :param router_prefix: Префикс путей роутера. Пример: /items
        :param name: Название роутера на английском. Пример: Items
        :param description: Описание роутера. Пример: Работа с объектами
        :param dependencies: Список глобальных зависимостей роутера
        """
        self._name = name
        self._description = description
        self._has_authentication = has_authentication

        if not dependencies:
            dependencies = list()
        self._api_router = APIRouter(
            prefix=router_prefix,
            dependencies=dependencies,
        )

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
