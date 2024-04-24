from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    url: str = Field()
    echo: bool = Field()

    model_config = SettingsConfigDict(env_prefix="SQL_DB_")


settings = Settings()
