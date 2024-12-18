from typing import Optional, List

from fastapi import Depends
from fastapi_cache.decorator import cache
from starlette import status

from src.controllers import ApartmentController
from src.controllers import AssistantController
from src.dependencies.controller_dependencies import get_apartment_controller
from src.dependencies.controller_dependencies import get_assistant_controller
from src.schemas.responses import DebtorMessageResponse, DebtorInfoResponse
from .unique_router import UniqueRouter

assistant_router = UniqueRouter(
            router_prefix='/assistant',
            name='Assistant',
            description='Уникальные методы для работы с должниками',
            has_authentication=False
        )


@assistant_router.api_router.get(
            path='/get_message_body_for_debtor',
            summary='Получение текста сообщения для отправки должнику',
            response_model=DebtorMessageResponse,
            status_code=status.HTTP_200_OK
        )
@cache(expire=60)
async def get_message_body_for_debtor(
        apartment_number: int,
        building_id: int,
        ap_controller: ApartmentController = Depends(get_apartment_controller),  # type: ignore
        main_controller: AssistantController = Depends(get_assistant_controller)
) -> DebtorMessageResponse:  # type: ignore[valid-type]
    """
    Одиночное формирование уведомления о долге по заранее известному новеру квартиры и id дома.
    """
    full_data_apart_dto = await ap_controller.get_apartments_full_data_with_debt_by_apart_id(
        apartment_number=apartment_number,
        building_id=building_id
    )
    return main_controller.map_data_to_debtor_message(full_data_apart_dto)


@assistant_router.api_router.get(
            path='/get_message_body_for_debtors',
            summary='Получение текста сообщения для отправки должникам',
            response_model=List[DebtorMessageResponse],
            status_code=status.HTTP_200_OK
        )
@cache(expire=60)
async def get_message_body_for_all_debtors(
        building_project_name: Optional[str] = None,
        ap_controller: ApartmentController = Depends(get_apartment_controller),  # type: ignore
        main_controller: AssistantController = Depends(get_assistant_controller)
) -> List[DebtorMessageResponse]:  # type: ignore[valid-type]
    """
    Метод работает по определенному ЖК либо по всем ЖК в целом, если building_project_name не передан.
    """

    full_data_apart_dto = await ap_controller.get_apartments_full_data_with_debt_by_project_name(building_project_name)
    return [main_controller.map_data_to_debtor_message(dto) for dto in full_data_apart_dto]


@assistant_router.api_router.get(
            path='/get_all_debtors_with_debt_analyse',
            summary='Получение списка должников с квартирами и данными о долге',
            response_model=List[DebtorInfoResponse],
            status_code=status.HTTP_200_OK
        )
@cache(expire=60)
async def get_all_debtors_with_debt_analyse(
        building_project_name: Optional[str] = None,
        ap_controller: ApartmentController = Depends(get_apartment_controller),  # type: ignore
        main_controller: AssistantController = Depends(get_assistant_controller)
) -> List[DebtorInfoResponse]:  # type: ignore[valid-type]
    """
    Поиск возможен по определенному ЖК либо по всем в целом.
    """
    full_data_apart_dto = await ap_controller.get_apartments_full_data_with_debt_by_project_name(building_project_name)
    return main_controller.map_debtors_info_response(dtos=full_data_apart_dto, sort_flag=True)
