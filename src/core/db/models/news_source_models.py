from typing import Any, Annotated

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .base import BaseModel


int_pk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, mapped_column(String(50))]


class NewsSource(BaseModel):
    id: Mapped[int_pk]
    source_type: Mapped[str_50]

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
    id: Mapped[int_pk] = mapped_column(ForeignKey(NewsSource.id))
    channel_handle: Mapped[str_50]
