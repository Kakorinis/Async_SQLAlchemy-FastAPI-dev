from settings import app_settings
from .mixin_auto_id_model import MixinAutoIdModel


class BaseDbModel(MixinAutoIdModel):
    """
    Базовая модель для ORM c автоинкрементным id.
    Используется для указания схемы.
    """

    __abstract__ = True
    __table_args__ = {
        'schema': app_settings.SQL_SCHEMA,
    }
