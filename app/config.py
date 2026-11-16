
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Gemini
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.5-flash-lite"

    # Telegram
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    # Mastodon
    mastodon_instance_url: str | None = None
    mastodon_access_token: str | None = None

    # Telegraph
    telegraph_access_token: str | None = None

    # DEV.to
    devto_api_key: str | None = None

    # Bluesky
    bluesky_handle: str | None = None
    bluesky_app_password: str | None = None
    bluesky_pds_url: str = "https://bsky.social"


settings = Settings()
