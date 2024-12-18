from typing import List

from pydantic import Field

from src.schemas.dtos import ApartmentSchema
from src.schemas.dtos import BillSchema


class ApartmentsDebtSchema(ApartmentSchema):
    address: str = Field(
        init_var=True,
        kw_only=True,
        description='Адрес дома'
    )
    project_name: str = Field(
        init_var=True,
        kw_only=True,
        description='Название ЖК'
    )
    common_debt: float = Field(
        init_var=True,
        kw_only=True,
        description='Общая сумма задолженности по квартире'
    )
    bills_not_payed: List[BillSchema]
