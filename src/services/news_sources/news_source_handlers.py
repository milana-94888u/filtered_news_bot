from abc import ABC, abstractmethod
from typing import Literal
from urllib.parse import urlparse

from utils.telegram import PublicTelegramChannelReader

from .schemas import NewsSourceData, PublicTelegramChannelState


class NewsSourceHandler(ABC):
    source_type: Literal["PublicTelegramChannel"]

    @abstractmethod
    async def get_unique_name_with_validation(
        self, news_source_identifier: str
    ) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_initial_data(
        self, news_source_identifier: str
    ) -> NewsSourceData | None:
        raise NotImplementedError


class PublicTelegramChannelHandler(NewsSourceHandler):
    source_type = "PublicTelegramChannel"

    def __init__(self, reader: PublicTelegramChannelReader) -> None:
        self.reader = reader

    @staticmethod
    def try_get_username_from_mention(mention: str) -> str | None:
        if not mention.startswith("@"):
            return None
        if not mention[1:].isidentifier():
            return None
        return mention[1:].lower()

    @staticmethod
    def try_get_username_from_url(url: str) -> str | None:
        parsed = urlparse(url)
        if parsed.netloc != "t.me":
            return None
        if not parsed.path.startswith("/"):
            return None
        initial, username, *remaining = parsed.path.split("/")
        if remaining:
            return None
        return username.lower()

    async def get_unique_name_with_validation(
        self, news_source_identifier: str
    ) -> str | None:
        return self.try_get_username_from_mention(
            news_source_identifier
        ) or self.try_get_username_from_url(news_source_identifier)

    async def get_initial_data(
        self, news_source_identifier: str
    ) -> NewsSourceData | None:
        username = await self.get_unique_name_with_validation(news_source_identifier)
        if username is None:
            return None
        last_post_id = await self.reader.get_last_post_id(username)
        return NewsSourceData(
            unique_name=username,
            state_data=PublicTelegramChannelState(last_post_id=last_post_id),
        )
