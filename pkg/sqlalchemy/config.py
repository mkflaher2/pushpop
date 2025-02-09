from typing import Any, Optional

from os import getenv
from pydantic import BaseModel, ConfigDict, Field, PostgresDsn, ValidationInfo, field_validator

class PostgresSettings(BaseModel):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = Field(default=None, validate_default=True)

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        url = PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            path=f"{values.data.get('POSTGRES_DB') or ''}"
        )
        return str(url)

    model_config = ConfigDict(case_sensitive=True, extra="ignore")

def load_postgres_settings() -> PostgresSettings:

    settings_dict = {
        "POSTGRES_HOST": getenv("POSTGRES_HOST"),
        "POSTGRES_PORT": getenv("POSTGRES_PORT"),
        "POSTGRES_USER": getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": getenv("POSTGRES_PASSWORD"),
        "POSTGRES_DB": getenv("POSTGRES_DB"),
    }

    return PostgresSettings(**settings_dict)

postgres_settings = load_postgres_settings()
