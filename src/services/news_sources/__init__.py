from abc import ABC, abstractmethod
from typing import Callable

from .schemas import NewsSourceData

from core.db.models import *
from core.db.db_helper import db_helper

from repositories.news_sources_respository import NewsSourcesRepository

from .news_source_handlers import NewsSourceHandler


class NewsSourcesServiceBase(ABC):
    @abstractmethod
    async def get_all_news_sources(self) -> list[NewsSource]:
        raise NotImplementedError

    @abstractmethod
    async def get_news_source(
        self, model: type[NewsSource], unique_name: str
    ) -> NewsSource:
        raise NotImplementedError

    @abstractmethod
    async def get_or_create_news_source(
        self, news_source_identifier: str
    ) -> NewsSourceData:
        raise NotImplementedError


class NewsSourcesService(NewsSourcesServiceBase):
    def __init__(
        self,
        news_sources_repository: Callable[[], NewsSourcesRepository],
        handlers: list[NewsSourceHandler],
    ) -> None:
        self.repository = news_sources_repository()
        self.handlers = handlers

    async def get_all_news_sources(self) -> list[NewsSource]:
        pass

    async def get_news_source(
        self, model: type[NewsSource], unique_name: str
    ) -> NewsSource:
        pass

    @staticmethod
    def determine_source_model_by_type(source_type: str) -> type[NewsSource]:
        match source_type:
            case "PublicTelegramChannel":
                return PublicTelegramChannel
            case _:
                raise ValueError(f"Incorrect source type - {source_type}")

    async def get_or_create_news_source(
        self, news_source_identifier: str
    ) -> NewsSourceData:
        for handler in self.handlers:
            if unique_name := await handler.get_unique_name_with_validation(
                news_source_identifier
            ):
                model = self.determine_source_model_by_type(handler.source_type)
                if news_source := await self.repository.try_get_news_source(
                    model, unique_name
                ):
                    return NewsSourceData(
                        unique_name=unique_name,
                        state_data=news_source,
                    )
                news_source_data = await handler.get_initial_data(
                    news_source_identifier
                )
                await self.add_news_source(news_source_data)
                return news_source_data

    async def add_news_source(self, data: NewsSourceData) -> None:
        model = self.determine_source_model_by_type(data.state_data.source_type)
        await self.repository.add_news_source(
            model, data.unique_name, data.state_data.model_dump(exclude={"source_type"})
        )
