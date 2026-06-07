"""
Statistics Service Module
Aggregates bot-wide statistics for the dashboard.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from config.database import get_db, check_db_health
from config.settings import settings

logger = logging.getLogger(__name__)


class StatsService:
    """Service for fetching and aggregating bot statistics."""

    def __init__(self):
        self.db = get_db()

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get all stats for the admin dashboard."""
        try:
            # Parallel stat fetching
            total_users = await self.db.users.count_documents({})

            cutoff_7d = datetime.utcnow() - timedelta(days=7)
            active_users = await self.db.users.count_documents({
                "last_activity": {"$gte": cutoff_7d},
                "is_banned": {"$ne": True}
            })

            total_posts = await self.db.posts.count_documents({})
            total_channels = await self.db.channels.count_documents({"is_active": True})
            total_broadcasts = await self.db.broadcasts.count_documents({})
            banned_users = await self.db.users.count_documents({"is_banned": True})

            db_health = await check_db_health()

            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_posts": total_posts,
                "total_channels": total_channels,
                "total_broadcasts": total_broadcasts,
                "banned_users": banned_users,
                "db_healthy": db_health.get("status") == "healthy",
                "maintenance_mode": settings.MAINTENANCE_MODE,
                "db_size_mb": db_health.get("data_size_mb", 0),
            }
        except Exception as e:
            logger.error(f"Error fetching stats: {e}")
            return {
                "total_users": 0, "active_users": 0, "total_posts": 0,
                "total_channels": 0, "total_broadcasts": 0, "banned_users": 0,
                "db_healthy": False, "maintenance_mode": False, "db_size_mb": 0,
            }

    async def get_broadcast_stats(self, broadcast_id: str) -> Dict[str, Any]:
        """Get statistics for a specific broadcast."""
        broadcast = await self.db.broadcasts.find_one({"broadcast_id": broadcast_id})
        if not broadcast:
            return {}
        return {
            "total": broadcast.get("total_users", 0),
            "sent": broadcast.get("sent_count", 0),
            "failed": broadcast.get("failed_count", 0),
            "blocked": broadcast.get("blocked_count", 0),
            "progress": broadcast.get("progress_pct", 0),
            "status": broadcast.get("status", "unknown"),
        }

    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get analytics for a specific post."""
        post = await self.db.posts.find_one({"post_id": post_id})
        if not post:
            return {}
        return {
            "views": post.get("views", 0),
            "forwards": post.get("forwards", 0),
            "reactions": post.get("reactions", 0),
            "channels": len(post.get("target_channels", [])),
            "published_at": post.get("published_at"),
        }

    async def get_user_growth(self, days: int = 7) -> Dict[str, int]:
        """Get user registration trend."""
        result = {}
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=i)
            start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            count = await self.db.users.count_documents({
                "joined_at": {"$gte": start, "$lt": end}
            })
            result[start.strftime("%Y-%m-%d")] = count
        return result
