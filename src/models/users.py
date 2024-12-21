from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base_db_model import BaseDbModel


class Users(BaseDbModel):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
