"""
Database Models Module
Pydantic models for all MongoDB collections with validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import uuid


def generate_id() -> str:
    return str(uuid.uuid4())[:8].upper()


# ── Enums ──────────────────────────────────────────────────────────────────


class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    DELETED = "deleted"


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class AdType(str, Enum):
    BANNER = "banner"
    TEXT = "text"
    MEDIA = "media"
    INLINE = "inline"


class BroadcastStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SecurityEventType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    FAILED_AUTH = "failed_auth"
    ADMIN_ACTION = "admin_action"
    BAN = "ban"
    UNBAN = "unban"
    FLOOD = "flood"
    SUSPICIOUS = "suspicious"
    PERMISSION_DENIED = "permission_denied"
    COMMAND = "command"


class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"
    ANIMATION = "animation"
    VOICE = "voice"
    VIDEO_NOTE = "video_note"
    STICKER = "sticker"


# ── User Model ──────────────────────────────────────────────────────────────


class UserModel(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    full_name: str = ""
    language_code: Optional[str] = "en"
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_banned: bool = False
    ban_reason: Optional[str] = None
    force_subscribed: bool = False
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    total_messages: int = 0
    ip_addresses: List[str] = []
    notes: Optional[str] = None
    custom_data: Dict[str, Any] = {}

    class Config:
        use_enum_values = True


# ── Post Model ──────────────────────────────────────────────────────────────


class InlineButton(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None


class ButtonRow(BaseModel):
    buttons: List[InlineButton] = []


class PostModel(BaseModel):
    post_id: str = Field(default_factory=generate_id)
    title: str
    content: Optional[str] = None
    media_file_id: Optional[str] = None
    media_type: Optional[MediaType] = None
    caption: Optional[str] = None
    button_rows: List[ButtonRow] = []
    target_channels: List[int] = []
    status: PostStatus = PostStatus.DRAFT
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    is_draft: bool = True
    clone_count: int = 0
    views: int = 0
    forwards: int = 0
    reactions: int = 0
    auto_caption_id: Optional[str] = None
    tags: List[str] = []

    class Config:
        use_enum_values = True


# ── Channel Model ───────────────────────────────────────────────────────────


class ChannelModel(BaseModel):
    channel_id: int
    channel_name: str
    channel_username: Optional[str] = None
    invite_link: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    member_count: int = 0
    total_posts: int = 0
    added_by: int
    added_at: datetime = Field(default_factory=datetime.utcnow)
    last_post_at: Optional[datetime] = None
    custom_footer: Optional[str] = None
    auto_caption_enabled: bool = False
    ad_enabled: bool = True


# ── Caption Template Model ──────────────────────────────────────────────────


class CaptionTemplateModel(BaseModel):
    caption_id: str = Field(default_factory=generate_id)
    name: str
    template: str
    footer: Optional[str] = None
    hashtags: List[str] = []
    dynamic_vars: Dict[str, str] = {}
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    usage_count: int = 0


# ── Link Model ──────────────────────────────────────────────────────────────


class LinkModel(BaseModel):
    link_id: str = Field(default_factory=generate_id)
    original_url: str
    short_url: Optional[str] = None
    referral_code: Optional[str] = None
    click_count: int = 0
    unique_clicks: int = 0
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_clicked: Optional[datetime] = None
    is_active: bool = True
    tags: List[str] = []
    click_data: List[Dict[str, Any]] = []


# ── Button Template Model ───────────────────────────────────────────────────


class ButtonTemplateModel(BaseModel):
    template_id: str = Field(default_factory=generate_id)
    name: str
    rows: List[ButtonRow] = []
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    usage_count: int = 0
    description: Optional[str] = None


# ── Advertisement Model ─────────────────────────────────────────────────────


class AdvertisementModel(BaseModel):
    ad_id: str = Field(default_factory=generate_id)
    title: str
    ad_type: AdType
    content: Optional[str] = None
    media_file_id: Optional[str] = None
    button_rows: List[ButtonRow] = []
    target_channels: List[int] = []
    priority: int = 5  # 1-10, higher = more priority
    is_active: bool = True
    rotation_slot: int = 5  # Show every N posts
    daily_budget: Optional[int] = None  # Max shows per day
    total_shows: int = 0
    today_shows: int = 0
    click_count: int = 0
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    schedule_start: Optional[datetime] = None
    schedule_end: Optional[datetime] = None

    class Config:
        use_enum_values = True


# ── Broadcast Model ─────────────────────────────────────────────────────────


class BroadcastModel(BaseModel):
    broadcast_id: str = Field(default_factory=generate_id)
    message_content: str
    media_file_id: Optional[str] = None
    media_type: Optional[str] = None
    button_rows: List[ButtonRow] = []
    target_users: str = "all"  # "all", "active", "role:<role>"
    status: BroadcastStatus = BroadcastStatus.PENDING
    started_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_users: int = 0
    sent_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    progress_pct: float = 0.0

    class Config:
        use_enum_values = True


# ── Security Log Model ──────────────────────────────────────────────────────


class SecurityLogModel(BaseModel):
    log_id: str = Field(default_factory=generate_id)
    user_id: int
    username: Optional[str] = None
    event_type: SecurityEventType
    description: str
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    extra_data: Dict[str, Any] = {}
    severity: str = "info"  # info, warning, critical

    class Config:
        use_enum_values = True


# ── Session Model ───────────────────────────────────────────────────────────


class SessionModel(BaseModel):
    user_id: int
    session_token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    ip_address: Optional[str] = None
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    login_attempts: int = 0
    is_active: bool = True


# ── Media Library Model ─────────────────────────────────────────────────────


class MediaLibraryModel(BaseModel):
    media_id: str = Field(default_factory=generate_id)
    file_id: str
    file_unique_id: str
    media_type: MediaType
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    caption: Optional[str] = None
    tags: List[str] = []
    uploaded_by: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    usage_count: int = 0

    class Config:
        use_enum_values = True


# ── Bot Settings Model ──────────────────────────────────────────────────────


class BotSettingModel(BaseModel):
    key: str
    value: Any
    description: Optional[str] = None
    updated_by: Optional[int] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ── Notification Model ──────────────────────────────────────────────────────


class NotificationModel(BaseModel):
    notif_id: str = Field(default_factory=generate_id)
    user_id: Optional[int] = None  # None = broadcast to all admins
    title: str
    message: str
    notif_type: str = "info"  # info, warning, error, success
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    action_url: Optional[str] = None
