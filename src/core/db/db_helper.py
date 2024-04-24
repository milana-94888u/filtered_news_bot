from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.db.models import *
from core.db.config import settings


class DBHelper:
    def __init__(self) -> None:
        self.engine = create_async_engine(url=settings.url, echo=settings.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )


db_helper = DBHelper()
