from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from .base_db_model import BaseDbModel


class Owner(BaseDbModel):
    __tablename__ = 'owner'

    fullname: Mapped[str] = mapped_column(String(100), nullable=False, comment='ФИО владельца')
    passport_series: Mapped[str] = mapped_column(String(4), nullable=False, comment='Серия паспорта')
    passport_values: Mapped[str] = mapped_column(String(6), nullable=False, comment='Номер паспорта')
    phone: Mapped[int] = mapped_column(String(11), nullable=False, unique=True, comment='Сотовый телефон')

    apartments: Mapped[List["Apartment"]] = relationship(  # type: ignore[name-defined] # noqa: F821
        'Apartment',
        back_populates='owner',
        lazy="joined",
        uselist=True
    )
