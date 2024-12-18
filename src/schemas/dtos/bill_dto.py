from pydantic import Field

from .bill_schema import BillSchema
from .mixin_id_schema import MixinIdSchema


class BillDto(MixinIdSchema, BillSchema):
    id_apartment: int = Field(
        init_var=True,
        kw_only=True,
        description='Идентификатор квартиры'
    )
