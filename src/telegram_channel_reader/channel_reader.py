import asyncio
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.patched import Message
from telethon.events import NewMessage

from telegram_channel_reader.config import settings


async def read_channel(client: TelegramClient, channel: str) -> None:
    last_post = await anext(client.iter_messages(channel, limit=1))
    print(last_post)
    return
    while True:
        async for message in client.iter_messages(channel, min_id=last_message_id):
            message: Message
            print(message.text)
            last_message_id = message.id


async def process_post(event):
    print(event)


async def main():
    async with TelegramClient(
        "session_name", settings.api_id, settings.api_hash.get_secret_value()
    ) as client:
        client: TelegramClient
        channel_id = await client.get_peer_id("onitenjikunezumi")
        print(channel_id)
        client.add_event_handler(process_post, NewMessage(chats=[channel_id]))
        await client.run_until_disconnected()
        # await read_channel(client, "onitenjikunezumi")


if __name__ == "__main__":
    asyncio.run(main())
