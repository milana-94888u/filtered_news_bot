import asyncio

from aiogram import Bot, Dispatcher, types

from core.db.db_helper import db_helper
from config import settings

bot = Bot(settings.http_api_token)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main() -> None:
    await db_helper.create_models()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
