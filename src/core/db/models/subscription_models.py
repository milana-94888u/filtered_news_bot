from typing import Any

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

from core.db.sql_types import int_primary_key, str_with_length
from .base import BaseModel


class TelegramUser(BaseModel):
    telegram_id: Mapped[int_primary_key]

    news_sources: Mapped[list["NewsSource"]] = relationship(
        secondary=lambda: Subscription.__table__, back_populates="subscribed_users"
    )


class NewsSource(BaseModel):
    source_type: Mapped[str_with_length(50)] = mapped_column(primary_key=True)
    unique_name: Mapped[str_with_length(50)] = mapped_column(primary_key=True)

    subscribed_users: Mapped[list["TelegramUser"]] = relationship(
        secondary=lambda: Subscription.__table__, back_populates="news_sources"
    )

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
                "inherit_condition": cls.source_type == cls.__name__
                and cls.unique_name == NewsSource.unique_name,
            }


class PublicTelegramChannel(NewsSource):
    source_type: Mapped[str_with_length(50)] = mapped_column(
        ForeignKey(NewsSource.source_type), primary_key=True
    )
    unique_name: Mapped[str_with_length(50)] = mapped_column(
        ForeignKey(NewsSource.unique_name), primary_key=True
    )
    last_post_id: Mapped[int]


class Subscription(BaseModel):
    user_id = mapped_column(ForeignKey(TelegramUser.telegram_id), primary_key=True)
    source_type: Mapped[str_with_length(50)] = mapped_column(primary_key=True)
    source_name: Mapped[str_with_length(50)] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            [source_type, source_name], [NewsSource.source_type, NewsSource.unique_name]
        ),
    )
