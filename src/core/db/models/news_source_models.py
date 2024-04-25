from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from core.db.sql_types import int_primary_key, str_with_length
from .base import BaseModel


class NewsSource(BaseModel):
    id: Mapped[int_primary_key]
    source_type: Mapped[str_with_length(50)]

    @classmethod
    @declared_attr.directive
    def __mapper_args__(cls: type["NewsSource"]) -> dict[str, Any]:
        if cls.__name__ == "Employee":
            return {
                "polymorphic_on": cls.source_type,
                "polymorphic_identity": cls.__name__,
            }
        else:
            return {"polymorphic_identity": cls.__name__}


class TelegramChannelSource(NewsSource):
    id: Mapped[int_primary_key] = mapped_column(ForeignKey(NewsSource.id))
    channel_handle: Mapped[str_with_length(50)]
