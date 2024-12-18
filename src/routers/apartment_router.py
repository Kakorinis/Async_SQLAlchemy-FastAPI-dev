from typing import List, Optional

from fastapi import Depends
from fastapi_cache.decorator import cache
from starlette import status

from src.controllers import ApartmentController
from src.dependencies.controller_dependencies import get_apartment_controller
from src.schemas.dtos import ApartmentDto
from src.schemas.dtos import ApartmentFullDto
from src.schemas.responses import ApartmentFullResponse
from .base_router import BaseRouter


class ApartmentRouter(BaseRouter):

    def __init__(self):
        super().__init__(
            router_prefix='/apartments',
            name='Apartments',
            description='Методы для работы с данными о квартирах',
            controller_dependency=Depends(get_apartment_controller),
            short_schema_type=ApartmentDto,
            external_schema_type=ApartmentFullDto,
        )

    def add_custom_routes(self):
        controller_dependency = self.controller_dependency

        """
        Метод позволяет получить массив квартир со всех домов, если не передать в параметре пути building_id:
        http://localhost:8000/apartments/get_apartments_with_debt, либо выборочно по конкретному дому, например:
        http://localhost:8000/apartments/get_apartments_with_debt?building_id=2
        """
        @self.api_router.get(
            path='/get_apartments_with_debt',
            summary='Получение квартир с коммунальной задолженностью',
            response_model=List[ApartmentFullResponse],
            status_code=status.HTTP_200_OK
        )
        @cache(expire=self.cache_lifetime)
        async def get_apartments_with_debt(
                building_id: Optional[int] = None,
                controller: ApartmentController = controller_dependency  # type: ignore
        ) -> List[ApartmentFullResponse]:  # type: ignore[valid-type]
            """
            Получение квартир с задолженностью.
            Возможно получить все квартиры всех домов, заведенных в БД либо точечно по конкретному дому.
            """
            return await controller.get_apartments_full_data_with_debt(building_id)


apartment_router = ApartmentRouter()
