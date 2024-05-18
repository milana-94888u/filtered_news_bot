from core.db.models import *
from core.db.db_helper import db_helper


class UsersRepository:
    def __init__(self) -> None:
        self.session_factory = db_helper.session_factory

    async def add_user(self, telegram_id: int, data: dict) -> None:
        async with self.session_factory() as session:
            session.add(
                TelegramUser(
                    telegram_id=telegram_id,
                    **data,
                )
            )
            await session.commit()

    async def try_get_user(self, telegram_id: int) -> TelegramUser | None:
        async with self.session_factory() as session:
            return await session.get(TelegramUser, (telegram_id,))
