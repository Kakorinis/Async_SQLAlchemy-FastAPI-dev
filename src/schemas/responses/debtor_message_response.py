from pydantic import Field

from src.schemas.dtos import BaseSchema
from settings import app_settings


class DebtorMessageResponse(BaseSchema):
    data: str = Field(
        examples=[app_settings.DEBTOR_MESSAGE_TEMPLATE]
    )
