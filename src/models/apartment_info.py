from sqlalchemy import ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .apartment import Apartment
from .base_db_model import BaseDbModel


class ApartmentInfo(BaseDbModel):
    __tablename__ = 'apartment_info'

    id_apartment: Mapped[int] = mapped_column(
        ForeignKey(Apartment.id, ondelete='CASCADE'),  # удалить при удалении квартиры
        nullable=False,
        comment='Идентификатор квартиры'
    )
    room_number: Mapped[int] = mapped_column(Integer, nullable=False, comment='Количество комнат')
    common_square: Mapped[float] = mapped_column(Float, nullable=False, comment='Общая площадь квартиры')
    kitchen_square: Mapped[float] = mapped_column(Float, nullable=True, comment='Площадь кухни')
    balcony: Mapped[bool] = mapped_column(Boolean, nullable=True, comment='Наличие балкона')
