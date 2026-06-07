"""
Configuration Settings Module
Loads all environment variables and provides typed settings.
"""


from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Bot Configuration ─────────────────────────────────────────
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token from @BotFather")
    BOT_USERNAME: str = Field(default="LalchandInkhiyaBot")

    # ── Admin Configuration ───────────────────────────────────────
    ADMIN_IDS: List[int] = Field(default=[], description="List of admin Telegram IDs")
    SUPER_ADMIN_ID: int = Field(..., description="Super admin Telegram ID")

    # ── MongoDB Configuration ─────────────────────────────────────
    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URI"
    )
    DB_NAME: str = Field(default="lalchand_inkhiya_db")

    # ── Security Configuration ────────────────────────────────────
    SECRET_KEY: str = Field(..., description="Secret key for session management")
    SESSION_TIMEOUT: int = Field(default=3600, description="Session timeout in seconds")
    MAX_LOGIN_ATTEMPTS: int = Field(default=5)
    FLOOD_RATE: int = Field(default=30, description="Max messages per minute")

    # ── Feature Flags ─────────────────────────────────────────────
    MAINTENANCE_MODE: bool = Field(default=False)
    FORCE_SUBSCRIBE: bool = Field(default=False)
    FORCE_SUBSCRIBE_CHANNEL: Optional[str] = Field(default=None)

    # ── URL Shortener ─────────────────────────────────────────────
    BITLY_TOKEN: Optional[str] = Field(default=None)
    TINYURL_API: Optional[str] = Field(default=None)

    # ── Storage ───────────────────────────────────────────────────
    MAX_FILE_SIZE_MB: int = Field(default=50)
    BACKUP_INTERVAL_HOURS: int = Field(default=24)

    # ── Logging ───────────────────────────────────────────────────
    LOG_LEVEL: str = Field(default="INFO")
    LOG_CHANNEL_ID: Optional[int] = Field(default=None, description="Channel to send logs to")

    # ── Ads Configuration ─────────────────────────────────────────
    AD_ROTATION_INTERVAL: int = Field(default=5, description="Show ad every N posts")

    @validator("ADMIN_IDS", pre=True)
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
