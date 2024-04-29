import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Bot, Dispatcher
from aiogram.types import Message, MessageEntity
from aiogram.filters import Command

from core.db.db_helper import db_helper
from core.db.models import *

from telegram_channel_reader.channel_reader import try_add_channel

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


async def get_or_register_channel(handle: str) -> TelegramChannelSource:
    async with db_helper.session_factory() as session:
        session: AsyncSession
        result = (
            await session.execute(
                select(TelegramChannelSource).where(
                    TelegramChannelSource.channel_handle == handle
                )
            )
        ).one_or_none()
        channel: TelegramChannelSource = result[0] if result else None
        if channel is None:
            channel = TelegramChannelSource(channel_handle=handle)
            session.add(channel)
            await session.commit()
        return channel


@dp.message(Command("add"))
async def cmd_add(message: Message) -> None:
    user = await get_or_register_user(message.from_user.id)
    entities = message.entities
    if len(entities) != 2:
        return
    if entities[1].type != "mention":
        return
    mention = message.text[entities[1].offset : entities[1].offset + entities[1].length]
    await try_add_channel(mention)


async def main() -> None:
    await db_helper.create_models()
    print("starting bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
