from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_id: int
    api_hash: SecretStr
    title: str
    short_name: str

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_APP_")


settings = Settings()
