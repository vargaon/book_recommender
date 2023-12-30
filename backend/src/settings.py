from functools import lru_cache
from typing import Annotated

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Api
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str,
        Field(title="Backend cors origins", description="Allowed CORS origins."),
    ] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Assemble backend cors origin into list structure."""

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list)):
            return v

        raise ValueError(v)

    # App
    EMBEDDING_MODEL: Annotated[
        str, Field(title="Model used for books description embedding")
    ] = "all-MiniLM-L12-v2"

    # Mongo
    MONGO_HOST: Annotated[
        str, Field(title="Mongo database host", description="Host address of mongo database.")
    ] = "localhost"

    MONGO_USERNAME: Annotated[
        str | None,
        Field(title="Mongo database username", description="Name of user of mongo database."),
    ] = None

    MONGO_PASSWORD: Annotated[
        str | None,
        Field(
            title="Mongo database user password", description="Password of mongo database user."
        ),
    ] = None

    MONGO_PORT: Annotated[int, Field(title="Mongo database port")] = 27017

    # Chroma
    CHROMA_HOST: Annotated[
        str, Field(title="Chroma database host", description="Host address of chroma database")
    ] = "localhost"

    CHROMA_PORT: Annotated[str, Field(title="Chroma database port")] = "8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


@lru_cache
def get_settings() -> Settings:
    """Get system setting

    :return: Settings of system
    :rtype: Settings
    """

    return Settings()
