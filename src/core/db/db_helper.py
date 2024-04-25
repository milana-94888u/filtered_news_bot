from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession,
)

from core.db.models import *
from core.db.config import settings


class DBHelper:
    def __init__(self) -> None:
        self.engine = create_async_engine(url=settings.url, echo=settings.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def create_models(self) -> None:
        async with self.engine.begin() as connection:
            connection: AsyncConnection
            await connection.run_sync(BaseModel.metadata.create_all)

    async def get_db_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = DBHelper()
