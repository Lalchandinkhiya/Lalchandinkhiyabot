"""Utility Helpers - Common helper functions."""
from datetime import datetime, timezone
from typing import Optional
from config.settings import settings


def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    return user_id == settings.SUPER_ADMIN_ID or user_id in settings.ADMIN_IDS


def require_super_admin(user_id: int) -> bool:
    """Check if a user is the super admin."""
    return user_id == settings.SUPER_ADMIN_ID


def format_uptime(start_time: datetime) -> str:
    """Format bot uptime as human-readable string."""
    now = datetime.now(timezone.utc)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    diff = now - start_time
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    else:
        return f"{minutes}m {seconds}s"


def format_number(n: int) -> str:
    """Format large numbers with commas."""
    return f"{n:,}"


def truncate(text: str, max_len: int = 50) -> str:
    """Truncate text to max length."""
    return text[:max_len] + "..." if len(text) > max_len else text


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def parse_button_text(text: str) -> list:
    """
    Parse button text format into rows of buttons.
    Format: "Text | URL || Text2 | URL2" (|| = same row, newline = new row)
    """
    rows = []
    for line in text.strip().split("\n"):
        row = []
        for btn_str in line.split("||"):
            parts = btn_str.strip().split("|", 1)
            if len(parts) == 2:
                btn_text = parts[0].strip()
                btn_url = parts[1].strip()
                if btn_text and btn_url:
                    row.append({"text": btn_text, "url": btn_url})
        if row:
            rows.append(row)
    return rows


def build_inline_keyboard(rows: list):
    """Build InlineKeyboardMarkup from parsed button rows."""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    for row in rows:
        btn_row = [
            InlineKeyboardButton(text=b["text"], url=b.get("url"),
                                  callback_data=b.get("callback_data"))
            for b in row
        ]
        builder.row(*btn_row)
    return builder.as_markup()
