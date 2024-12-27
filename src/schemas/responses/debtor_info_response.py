from typing import List

from pydantic import Field

from src.schemas.dtos import BaseSchema
from .apartments_debt_schema import ApartmentsDebtSchema


class DebtorInfoResponse(BaseSchema):
    """
    Схема
    """
    id_owner: int = Field(
        init_var=True,
        kw_only=True,
        description='Идентификатор владельца',
        default=None
    )
    fullname: str = Field(
        init_var=True,
        kw_only=True,
        description='ФИО владельца'
    )
    phone: str = Field(
        init_var=True,
        kw_only=True,
        description='Сотовый телефон'
    )

    all_aparts_common_debt: float = Field(
        init_var=True,
        kw_only=True,
        description='Общая сумма задолженности всех квартир персоны'
    )

    apartments_debt: List[ApartmentsDebtSchema]
