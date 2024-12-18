from typing import Optional

from pydantic import Field
from pydantic import field_validator

from .apartment_shema import ApartmentSchema
from .mixin_id_schema import MixinIdSchema


class ApartmentDto(MixinIdSchema, ApartmentSchema):

    id_building: int = Field(
        init_var=True,
        kw_only=True,
        description='Идентификатор дома'
    )
    id_owner: Optional[int] = Field(
        init_var=True,
        kw_only=True,
        description='Идентификатор владельца',
        default=None
    )

    @field_validator('id_owner', mode='before')
    @classmethod
    def validate_id_owner(cls, data: None | int) -> str | None:
        if isinstance(data, int):
            if data == 0:
                return None
        return data
