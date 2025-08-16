from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseModel):
    secret_key: str


class PostgresSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    db: str

    provider: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def localhost_url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@localhost:{self.port}/{self.db}"


class Settings(BaseSettings):
    postgres: PostgresSettings
    jwt: JwtSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()  # type: ignore
