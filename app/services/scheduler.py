"""
Scheduled Tasks Module
Background tasks: scheduled posts, auto backup, ad rotation.
"""
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot

logger = logging.getLogger(__name__)


async def run_scheduler(bot: Bot) -> None:
    """Main scheduler loop running in background."""
    logger.info("📅 Scheduler started")
    while True:
        try:
            await asyncio.gather(
                _process_scheduled_posts(bot),
                _process_scheduled_ads(bot),
                _auto_backup_check(),
                return_exceptions=True
            )
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        await asyncio.sleep(60)  # Run every minute


async def _process_scheduled_posts(bot: Bot) -> None:
    """Publish posts that are due."""
    from config.database import get_db
    from app.services.post_service import PostService

    svc = PostService()
    due_posts = await svc.get_due_scheduled_posts()

    for post in due_posts:
        try:
            channels = post.get("target_channels", [])
            for channel_id in channels:
                content = post.get("content", "")
                if post.get("media_file_id") and post.get("media_type") == "photo":
                    await bot.send_photo(
                        channel_id, post["media_file_id"], caption=content
                    )
                elif post.get("media_file_id") and post.get("media_type") == "video":
                    await bot.send_video(
                        channel_id, post["media_file_id"], caption=content
                    )
                elif content:
                    await bot.send_message(channel_id, content)

            await svc.update_post(
                post["post_id"],
                status="published",
                is_draft=False,
                published_at=datetime.utcnow()
            )
            logger.info(f"✅ Published scheduled post {post['post_id']}")
        except Exception as e:
            logger.error(f"Failed to publish post {post.get('post_id')}: {e}")
            await svc.update_post(post["post_id"], status="failed")


async def _process_scheduled_ads(bot: Bot) -> None:
    """Process scheduled advertisement delivery."""
    from config.database import get_db
    db = get_db()
    now = datetime.utcnow()

    active_ads = await db.advertisements.find({
        "is_active": True,
        "$or": [
            {"schedule_start": {"$lte": now}, "schedule_end": {"$gte": now}},
            {"schedule_start": None, "schedule_end": None},
        ],
        "expires_at": {"$gt": now}
    }).to_list(length=20)

    for ad in active_ads:
        if ad.get("expires_at") and ad["expires_at"] < now:
            await db.advertisements.update_one(
                {"ad_id": ad["ad_id"]}, {"$set": {"is_active": False}}
            )


async def _auto_backup_check() -> None:
    """Check if automatic backup is needed."""
    from config.database import get_db
    from config.settings import settings
    db = get_db()

    setting = await db.bot_settings.find_one({"key": "last_auto_backup"})
    if setting:
        last_backup = setting.get("value")
        if isinstance(last_backup, datetime):
            hours_since = (datetime.utcnow() - last_backup).total_seconds() / 3600
            if hours_since < settings.BACKUP_INTERVAL_HOURS:
                return

    # Record that backup was checked
    await db.bot_settings.update_one(
        {"key": "last_auto_backup"},
        {"$set": {"key": "last_auto_backup", "value": datetime.utcnow()}},
        upsert=True
    )
    logger.info("💾 Auto backup checkpoint recorded")
