from sqlalchemy.orm import Mapped

from core.db.sql_types import int_primary_key, str_with_length
from .base import BaseModel


class TelegramUser(BaseModel):
    id: Mapped[int_primary_key]
