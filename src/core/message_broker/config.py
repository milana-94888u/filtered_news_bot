from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str
    posts_queue_name: str

    model_config = SettingsConfigDict(env_prefix="RABBITMQ_")


settings = Settings()
