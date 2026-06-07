"""Notification Service - Sends system notifications to admins."""
import logging
from datetime import datetime
from aiogram import Bot
from config.settings import settings
from config.database import get_db

logger = logging.getLogger(__name__)


async def notify_admins_startup(bot: Bot) -> None:
    """Notify all admins that the bot has started."""
    admin_ids = list(set(settings.ADMIN_IDS + [settings.SUPER_ADMIN_ID]))
    text = (
        f"✅ <b>Bot Started Successfully!</b>\n\n"
        f"🤖 <b>LALCHAND INKHIYA BOT</b>\n"
        f"🕐 Time: <code>{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</code>\n"
        f"🔱 Version: <code>v2.0.0</code>\n"
        f"🗃️ Database: <code>Connected ✅</code>\n"
        f"⚡ Status: <code>Online 🟢</code>"
    )
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")


async def notify_admins_shutdown(bot: Bot) -> None:
    """Notify all admins that the bot is shutting down."""
    admin_ids = list(set(settings.ADMIN_IDS + [settings.SUPER_ADMIN_ID]))
    text = (
        f"🛑 <b>Bot is shutting down!</b>\n\n"
        f"🕐 Time: <code>{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</code>"
    )
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            pass


async def send_notification(bot: Bot, user_id: int, title: str, message: str,
                             notif_type: str = "info") -> None:
    """Send a notification to a specific user and save to DB."""
    db = get_db()
    from app.models.models import NotificationModel
    notif = NotificationModel(
        user_id=user_id, title=title, message=message, notif_type=notif_type
    )
    await db.notifications.insert_one(notif.dict())
    icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}
    icon = icons.get(notif_type, "🔔")
    try:
        await bot.send_message(user_id, f"{icon} <b>{title}</b>\n\n{message}")
    except Exception as e:
        logger.warning(f"Failed to send notification to {user_id}: {e}")
