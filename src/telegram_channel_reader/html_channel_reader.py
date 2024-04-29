import asyncio
from itertools import chain
from typing import Iterable

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag, NavigableString

from telegram_channel_reader.schemas import BaseNewPostData, NewPostsRequest


class HtmlTelegramPostsReader:
    def get_post_text(self, post_tag: Tag) -> str:
        post_text_tags = post_tag.find_all(class_="tgme_widget_message_text")
        if not post_text_tags:
            return ""  # no text in the post
        result_post_text_tag: Tag = post_text_tags[
            -1
        ]  # the last text tag is used to avoid nested tags and replied message tags
        return "☐".join(
            child
            for child in result_post_text_tag.contents
            if isinstance(child, NavigableString)
        )  # use placeholder on place of non-text elements

    def get_post_data(self, post_tag: Tag) -> BaseNewPostData:
        post_id = int(post_tag.attrs.get("data-post").split("/")[-1])
        text = self.get_post_text(post_tag)
        return BaseNewPostData(post_id=post_id, text=text)

    def extract_posts_from_html_preview(
        self, html_preview: str
    ) -> Iterable[BaseNewPostData]:
        soup = BeautifulSoup(html_preview, features="lxml")
        return map(self.get_post_data, soup.find_all(class_="tgme_widget_message"))

    async def get_new_posts_from_channel(
        self, session: ClientSession, request: NewPostsRequest
    ) -> Iterable[BaseNewPostData]:
        async with session.get(
            f"https://t.me/s/{request.channel_username}"
        ) as response:
            return filter(
                lambda post_data: post_data.post_id > request.last_post_id,
                self.extract_posts_from_html_preview(await response.text()),
            )

    async def get_new_posts(self, requests: list[NewPostsRequest]):
        async with ClientSession() as session:
            lists = []
            for request in requests:
                lists.append(await self.get_new_posts_from_channel(session, request))
            return list(chain(*lists))


async def main():
    print(
        await reader.get_new_posts(
            [NewPostsRequest(channel_username="onitenjikunezumi", last_post_id=4050)]
        )
    )


if __name__ == "__main__":
    reader = HtmlTelegramPostsReader()
    asyncio.run(main())
