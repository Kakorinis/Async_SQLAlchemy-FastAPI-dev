from fastapi import Depends

from src.controllers import ApartmentController
from src.controllers import AssistantController
from src.controllers import BillController
from src.controllers import BuildingController
from src.controllers import OwnerController
from src.dependencies.repository_dependencies import get_apartment_repository
from src.dependencies.repository_dependencies import get_assistant_repository
from src.dependencies.repository_dependencies import get_bill_repository
from src.dependencies.repository_dependencies import get_building_repository
from src.dependencies.repository_dependencies import get_owner_repository
from src.repositories import ApartmentRepository
from src.repositories import AssistantRepository
from src.repositories import BillRepository
from src.repositories import BuildingRepository
from src.repositories import OwnerRepository


async def get_apartment_controller(
        repository: ApartmentRepository = Depends(get_apartment_repository)
):
    """
    Фабрика ApartmentController для работы с таблицами квартир.

    :param repository: Репозиторий.
    :return: Контроллер.
    """
    return ApartmentController(main_repository=repository)


async def get_owner_controller(
        repository: OwnerRepository = Depends(get_owner_repository)
):
    """
    Фабрика OwnerController для работы с таблицами владельцев.

    :param repository: Репозиторий.
    :return: Контроллер.
    """
    return OwnerController(main_repository=repository)


async def get_bill_controller(
        repository: BillRepository = Depends(get_bill_repository)
):
    """
    Фабрика BillController для работы с таблицами квитанций.

    :param repository: Репозиторий.
    :return: Контроллер.
    """
    return BillController(main_repository=repository)


async def get_building_controller(
        repository: BuildingRepository = Depends(get_building_repository)
):
    """
    Фабрика BuildingController для работы с таблицами домов.

    :param repository: Репозиторий.
    :return: Контроллер.
    """
    return BuildingController(main_repository=repository)


async def get_assistant_controller(
        repository: AssistantRepository = Depends(get_assistant_repository)
):
    """
    Фабрика BuildingController для работы с таблицами домов.

    :param repository: Репозиторий.
    :return: Контроллер.
    """
    return AssistantController(main_repository=repository)
