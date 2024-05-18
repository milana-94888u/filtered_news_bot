from sqlalchemy import select

from core.db.models import *
from core.db.db_helper import db_helper


class NewsSourcesRepository:
    def __init__(self) -> None:
        self.session_factory = db_helper.session_factory

    async def add_news_source(
        self, model: type[NewsSource], unique_name: str, data: dict
    ) -> None:
        async with self.session_factory() as session:
            session.add(
                model(
                    unique_name=unique_name,
                    **data,
                )
            )
            await session.commit()

    async def try_get_news_source(
        self, model: type[NewsSource], unique_name: str
    ) -> NewsSource | None:
        async with self.session_factory() as session:
            return await session.get(model, (model.__name__, unique_name))
