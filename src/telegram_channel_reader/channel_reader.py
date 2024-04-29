import asyncio
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from telethon import TelegramClient
from telethon.tl.patched import Message
from telethon.types import Channel

from core.db.db_helper import db_helper
from core.db.models import *

from core.message_broker.producer import Producer

from telegram_channel_reader.config import settings


async def read_channels(client: TelegramClient) -> None:
    async with db_helper.session_factory() as session:
        session: AsyncSession
        channels: list[TelegramChannelSource] = [
            row[0]
            for row in (await session.execute(select(TelegramChannelSource))).all()
        ]
        for channel in channels:
            await read_channel(client, channel.channel_handle, channel.last_post_id)


async def read_channel(
    client: TelegramClient, channel_username: str, last_post_id: int
) -> None:
    producer = Producer("new_posts")
    async for message in client.iter_messages(channel_username, min_id=last_post_id):
        producer.publish(message.text)
    producer.close()


async def process_post(event):
    print(event)


async def main():
    await db_helper.create_models()
    async with TelegramClient(
        "session_name", settings.api_id, settings.api_hash.get_secret_value()
    ) as client:
        client: TelegramClient
        while True:
            await read_channels(client)
            await asyncio.sleep(5)


async def get_or_register_channel(
    handle: str, last_post_id: int
) -> TelegramChannelSource:
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
            channel = TelegramChannelSource(
                source_type="TelegramChannelSource",
                channel_handle=handle,
                last_post_id=last_post_id,
            )
            session.add(channel)
            await session.commit()
        return channel


async def get_channel_last_post_id(
    client: TelegramClient, channel_username: str
) -> int:
    last_post = await anext(client.iter_messages(channel_username, limit=1))
    last_post: Message
    return last_post.id


async def try_add_channel(possible_username: str) -> None:
    async with TelegramClient(
        "session_name", settings.api_id, settings.api_hash.get_secret_value()
    ) as client:
        client: TelegramClient
        entity = await client.get_entity(possible_username)
        if not isinstance(entity, Channel):
            return
        last_post_id = await get_channel_last_post_id(client, entity.username)
        await get_or_register_channel(entity.username, last_post_id)


if __name__ == "__main__":
    asyncio.run(main())
