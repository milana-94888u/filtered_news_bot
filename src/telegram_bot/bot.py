import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from core.db.db_helper import db_helper
from core.db.models import *
from config import settings

bot = Bot(settings.http_api_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    async with db_helper.session_factory() as session:
        session: AsyncSession
        user = await session.get(TelegramUser, message.from_user.id)
        if user:
            await message.answer("Registered")
        else:
            session.add(TelegramUser(id=message.from_user.id))
            await session.commit()


async def main() -> None:
    await db_helper.create_models()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
