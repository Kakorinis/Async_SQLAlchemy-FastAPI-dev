from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import ApartmentRepository
from src.repositories import AssistantRepository
from src.repositories import BillRepository
from src.repositories import BuildingRepository
from src.repositories import OwnerRepository
from .common import sqlalchemy_async_session_generator


async def get_apartment_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика ApartmentRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий ApartmentRepository.
    """
    return ApartmentRepository(async_db_session=async_db_session)


async def get_owner_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика OwnerRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий ApartmentRepository.
    """
    return OwnerRepository(async_db_session=async_db_session)


async def get_bill_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика BillRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий ApartmentRepository.
    """
    return BillRepository(async_db_session=async_db_session)


async def get_building_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика BuildingRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий ApartmentRepository.
    """
    return BuildingRepository(async_db_session=async_db_session)


async def get_assistant_repository(
        async_db_session: AsyncSession = Depends(sqlalchemy_async_session_generator)
):
    """
    Фабрика AssistantRepository.

    :param async_db_session: Асинхронная сессия SQLAlchemy.
    :return: Репозиторий ApartmentRepository.
    """
    return AssistantRepository(async_db_session=async_db_session)
