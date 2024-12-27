from typing import Optional

from .base_schema import BaseSchema


class ErrorSchema(BaseSchema):
    wrong_data_key: Optional[str] = None
    data: str | dict
    reason: str
