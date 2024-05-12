from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from core.db.sql_types import str_with_length
from .base import BaseModel


class NewsSource(BaseModel):
    source_type: Mapped[str_with_length(50)] = mapped_column(primary_key=True)
    unique_name: Mapped[str_with_length(50)] = mapped_column(primary_key=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source_type = self.__class__.__name__

    @declared_attr.directive
    def __mapper_args__(cls: type["NewsSource"]) -> dict[str, Any]:
        if cls.__name__ == "NewsSource":
            return {
                "polymorphic_identity": cls.__name__,
                "polymorphic_on": cls.source_type,
            }
        else:
            return {
                "polymorphic_identity": cls.__name__,
                "inherit_condition": cls.source_type == "TelegramChannelSource"
                and cls.unique_name == NewsSource.unique_name,
            }


class PublicTelegramChannelNewsSource(NewsSource):
    source_type: Mapped[str_with_length(50)] = mapped_column(
        ForeignKey(NewsSource.source_type), primary_key=True
    )
    unique_name: Mapped[str_with_length(50)] = mapped_column(
        ForeignKey(NewsSource.unique_name), primary_key=True
    )
    last_post_id: Mapped[int]
