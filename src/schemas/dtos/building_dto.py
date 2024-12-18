from pydantic import Field

from .mixin_id_schema import MixinIdSchema


class BuildingDto(MixinIdSchema):

    address: str = Field(
        init_var=True,
        kw_only=True,
        description='Адрес дома'
    )
    floors_number: int = Field(
        init_var=True,
        kw_only=True,
        description='Количество этажей'
    )
    lift_number: int = Field(
        init_var=True,
        kw_only=True,
        description='Количество лифтов'
    )
    project_name: str = Field(
        init_var=True,
        kw_only=True,
        description='Название ЖК'
    )
