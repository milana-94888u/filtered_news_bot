from abc import ABC, abstractmethod
from typing import Iterable

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag, NavigableString

from .schemas import BasePostData


class PublicTelegramChannelReader(ABC):
    @abstractmethod
    async def get_last_post_id(self, username: str) -> int:
        raise NotImplementedError


class HtmlPublicTelegramChannelReader(PublicTelegramChannelReader):
    @staticmethod
    def get_post_text(post_tag: Tag) -> str:
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

    def get_post_data(self, post_tag: Tag) -> BasePostData:
        post_id = int(post_tag.attrs.get("data-post").split("/")[-1])
        text = self.get_post_text(post_tag)
        return BasePostData(post_id=post_id, text=text)

    def extract_posts_from_html_preview(
        self, html_preview: str
    ) -> Iterable[BasePostData]:
        soup = BeautifulSoup(html_preview, features="lxml")
        return map(self.get_post_data, soup.find_all(class_="tgme_widget_message"))

    @staticmethod
    def build_channel_url(username: str, from_post_id: int | None = None) -> str:
        if from_post_id is None:
            return f"https://t.me/s/{username}"
        return f"https://t.me/s/{username}/{from_post_id}"

    async def get_last_post_id(self, username: str) -> int:
        async with ClientSession() as session:
            async with session.get(self.build_channel_url(username)) as response:
                last_posts = self.extract_posts_from_html_preview(await response.text())
                return max(post.post_id for post in last_posts)
