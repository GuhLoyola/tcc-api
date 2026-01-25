import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    PostgresDsn,
    Field
)

from pydantic_core import MultiHostUrl


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="ignore",
        env_ignore_empty = True,
    )
    PROJECT_NAME: str = "TrustLink-API"
    API_VERSION: str = "v2"
    DOMAIN: str = 'localhost'
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    JWT_SECRET_KEY: str
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    MODEL_PATH: Path = Path(os.getenv("MODEL_PATH", BASE_DIR / "ml" / "model" / "rf_model.pkl"))
    ENCODER_PATH: Path = Path(os.getenv("ENCODER_PATH", BASE_DIR / "ml" / "model" /  "label_encoder.pkl"))
    ORIGINAL_DATASET_PATH: Path = Path(os.getenv("DATASET_PATH", BASE_DIR / "ml" / "model" /  "dataset" / "malicious_phish.csv"))
    DATASET_PATH: Path = Path(os.getenv("DATASET_PATH", BASE_DIR / "ml" / "model" /  "dataset" / "normalized_dataset.csv"))

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = Field(default_factory=list)

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_SERVER: str
    POSTGRESQL_PORT: int
    POSTGRESQL_DATABASE: str

    @computed_field 
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRESQL_USERNAME,
            password=self.POSTGRESQL_PASSWORD,
            host=self.POSTGRESQL_SERVER,
            port=self.POSTGRESQL_PORT,
            path=self.POSTGRESQL_DATABASE,
        )
