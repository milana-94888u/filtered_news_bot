from typing import Literal
from abc import abstractmethod
from functools import cached_property

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SqlEngineSettings(BaseSettings):
    @abstractmethod
    def get_url(self) -> str:
        raise NotImplementedError


class PostgresSettings(SqlEngineSettings):
    db: str
    user: str
    password: SecretStr
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    def get_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class SqliteSettings(SqlEngineSettings):
    file_path: str

    model_config = SettingsConfigDict(env_prefix="SQLITE_")

    def get_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.file_path}"


class Settings(BaseSettings):
    engine: Literal["sqlite", "postgresql"]
    echo: bool

    @cached_property
    def url(self) -> str:
        engine_settings_factory: type[SqlEngineSettings] = SqlEngineSettings
        match self.engine:
            case "sqlite":
                engine_settings_factory = SqliteSettings
            case "postgresql":
                engine_settings_factory = PostgresSettings
        return engine_settings_factory().get_url()

    model_config = SettingsConfigDict(env_prefix="SQL_DB_")


settings = Settings()
