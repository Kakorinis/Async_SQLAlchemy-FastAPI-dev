from typing import List

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base_db_model import BaseDbModel


class Building(BaseDbModel):
    __tablename__ = 'building'

    address: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, comment='Адрес дома')
    floors_number: Mapped[int] = mapped_column(Integer, nullable=False, comment='Количество этажей')
    lift_number: Mapped[int] = mapped_column(Integer, nullable=False, comment='Количество лифтов')
    project_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Название ЖК')

    apartments: Mapped[List["Apartment"]] = relationship(  # type: ignore[name-defined] # noqa: F821
        'Apartment',
        back_populates='building',
        lazy="joined",
        uselist=True,
        cascade='all, delete-orphan'
    )
