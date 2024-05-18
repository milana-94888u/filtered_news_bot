import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from core.db.db_helper import db_helper

from services.news_sources import NewsSourcesServiceBase
from services.users import UserData
from telegram_bot.config import settings
from telegram_bot.middlewares.service import (
    NewsSourcesServiceMiddleware,
    UsersServiceMiddleware,
)
from telegram_bot.middlewares.user_registration import RegistrationMiddleware

bot = Bot(settings.api_token)
dp = Dispatcher()


@dp.message(Command("subscribe"))
async def cmd_subscribe(
    message: Message,
    command: CommandObject,
    news_sources_service: NewsSourcesServiceBase,
    user_data: UserData,
) -> None:
    print(user_data)
    print(await news_sources_service.get_or_create_news_source(command.args))


async def main() -> None:
    await db_helper.create_models()
    print("starting bot")
    dp.message.middleware(NewsSourcesServiceMiddleware())
    dp.message.middleware(UsersServiceMiddleware())
    dp.message.middleware(RegistrationMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
