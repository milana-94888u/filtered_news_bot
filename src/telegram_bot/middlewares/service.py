from typing import Callable, Dict, Awaitable, Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, TelegramObject

from services.news_sources import NewsSourcesService, NewsSourcesServiceBase
from services.users import UsersService, UsersServiceBase
from services.news_sources.news_source_handlers import PublicTelegramChannelHandler
from repositories.news_sources_respository import NewsSourcesRepository
from repositories.users_repository import UsersRepository
from utils.telegram import HtmlPublicTelegramChannelReader


class NewsSourcesServiceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.service: NewsSourcesServiceBase = NewsSourcesService(
            lambda: NewsSourcesRepository(),
            [PublicTelegramChannelHandler(HtmlPublicTelegramChannelReader())],
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Awaitable[Any]:
        data["news_sources_service"] = self.service
        return await handler(event, data)


class UsersServiceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.service: UsersServiceBase = UsersService(
            lambda: UsersRepository(),
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Awaitable[Any]:
        data["users_service"] = self.service
        return await handler(event, data)
