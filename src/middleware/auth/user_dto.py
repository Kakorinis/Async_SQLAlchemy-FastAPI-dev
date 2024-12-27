from src.schemas.dtos import BaseSchema


class UserDto(BaseSchema):
    login: str
    hashed_password: str
