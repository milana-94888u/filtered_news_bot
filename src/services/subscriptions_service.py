from core.db.models import *
from core.db.db_helper import db_helper


class SubscriptionsService:
    def __init__(self, news_sources_service, users_service):
        self.session_factory = db_helper.session_factory

    async def subscribe_user_to_source(self, user, source) -> None:
        pass
