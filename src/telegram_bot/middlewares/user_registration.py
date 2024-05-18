from typing import Callable, Dict, Awaitable, Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User

from services.users import UserData, UsersServiceBase


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        user: User = data["event_from_user"]
        service: UsersServiceBase = data["users_service"]
        data["user_data"] = await service.get_or_register_user(user.id)
        return await handler(event, data)
