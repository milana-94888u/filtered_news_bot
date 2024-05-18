from abc import ABC, abstractmethod
from typing import Callable

from .schemas import UserData

from repositories.users_repository import UsersRepository


class UsersServiceBase(ABC):
    @abstractmethod
    async def get_or_register_user(self, telegram_id: int) -> UserData:
        raise NotImplementedError


class UsersService(UsersServiceBase):
    def __init__(
        self,
        users_repository: Callable[[], UsersRepository],
    ) -> None:
        self.repository = users_repository()

    async def get_or_register_user(self, telegram_id: int) -> UserData:
        if user := await self.repository.try_get_user(telegram_id):
            return UserData(telegram_id=user.telegram_id)
        await self.repository.add_user(telegram_id, {})
        return UserData(telegram_id=telegram_id)
