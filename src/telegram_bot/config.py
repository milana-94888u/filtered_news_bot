from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_username: str = Field()
    http_api_token: str = Field()

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")


settings = Settings()
