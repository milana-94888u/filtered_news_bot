import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from core.db.db_helper import db_helper
from core.db.models import *
from config import settings

bot = Bot(settings.api_token)
dp = Dispatcher()


async def get_or_register_user(user_id: int) -> TelegramUser:
    async with db_helper.session_factory() as session:
        session: AsyncSession
        user = await session.get(TelegramUser, user_id)
        if user is None:
            user = TelegramUser(id=user_id)
            session.add(user)
            await session.commit()
        return user


@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    print(message)


async def main() -> None:
    await db_helper.create_models()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
