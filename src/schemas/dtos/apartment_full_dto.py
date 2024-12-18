from .apartment_dto import ApartmentDto
from .apartment_info_dto import ApartmentInfoDto


class ApartmentFullDto(ApartmentDto):
    apartment_info: ApartmentInfoDto
