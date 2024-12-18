from typing import List

from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from .base_db_model import BaseDbModel
from .building import Building
from .owner import Owner


class Apartment(BaseDbModel):
    __tablename__ = 'apartment'

    __table_args__ = (  # type: ignore[assignment]
        UniqueConstraint('id_building', 'utility_account', name='unique_id_building_utility_account'),
        BaseDbModel.__table_args__,
    )
    id_building: Mapped[int] = mapped_column(
        ForeignKey(Building.id, ondelete='CASCADE'),  # удалить все квартиры при удалении дома
        nullable=False,
        comment='Идентификатор дома'
    )
    id_owner: Mapped[int] = mapped_column(
        ForeignKey(Owner.id, ondelete='SET NULL'),
        nullable=True,
        comment='Идентификатор владельца'
    )
    utility_account: Mapped[str] = mapped_column(String(100), nullable=False, comment='Лицевой счет')
    apartment_number: Mapped[int] = mapped_column(Integer, nullable=False, comment='Номер квартиры')
    floor: Mapped[int] = mapped_column(Integer, nullable=False, comment='Этаж')

    apartment_info: Mapped["ApartmentInfo"] = relationship(  # type: ignore[name-defined] # noqa: F821
        'ApartmentInfo',
        lazy="joined",
        single_parent=True,
        cascade='all, delete-orphan'
    )
    building: Mapped[Building] = relationship(
        'Building',
        back_populates='apartments',
        lazy="joined",
        single_parent=True,

    )
    owner: Mapped["Owner"] = relationship(  # type: ignore[name-defined] # noqa: F821
        'Owner',
        back_populates='apartments',
        lazy="joined",
        single_parent=True,
        cascade='all, delete-orphan'
    )

    bills: Mapped[List["Bill"]] = relationship(  # type: ignore[name-defined] # noqa: F821
        'Bill',
        # foreign_keys=[id_building, utility_account],  # связь по составному ключу
        lazy="joined",
        uselist=True
    )
