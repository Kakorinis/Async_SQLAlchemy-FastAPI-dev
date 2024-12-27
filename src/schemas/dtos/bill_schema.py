from pydantic import Field

from .base_schema import BaseSchema


class BillSchema(BaseSchema):
    bill_period: str = Field(
        init_var=True,
        kw_only=True,
        description='Период начисления'
    )
    bill_size: float = Field(
        init_var=True,
        kw_only=True,
        description='Сумма начисления'
    )
    is_paid: bool = Field(
        init_var=True,
        kw_only=True,
        description='Флаг факта оплаты'
    )
