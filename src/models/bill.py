from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .apartment import Apartment
from .base_db_model import BaseDbModel


class Bill(BaseDbModel):
    __tablename__ = 'bill'

    id_apartment: Mapped[int] = mapped_column(
        ForeignKey(Apartment.id),
        nullable=False,
        comment='Идентификатор квартиры'
    )
    bill_period: Mapped[str] = mapped_column(String(100), nullable=False, comment='Период начисления')
    bill_size: Mapped[float] = mapped_column(Float, nullable=False, comment='Сумма начисления')
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False, comment='Флаг факта оплаты')
