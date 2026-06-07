"""
Post Service Module
All database operations for posts management.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from config.database import get_db
from app.models.models import PostModel, PostStatus

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db.posts

    async def create_post(self, title: str, content: Optional[str], created_by: int,
                           media_file_id: Optional[str] = None, media_type: Optional[str] = None) -> Dict:
        post = PostModel(
            title=title, content=content, created_by=created_by,
            media_file_id=media_file_id, media_type=media_type,
            is_draft=True, status=PostStatus.DRAFT
        )
        await self.collection.insert_one(post.dict())
        return post.dict()

    async def get_post(self, post_id: str) -> Optional[Dict]:
        return await self.collection.find_one({"post_id": post_id})

    async def update_post(self, post_id: str, **kwargs) -> bool:
        kwargs["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one({"post_id": post_id}, {"$set": kwargs})
        return result.modified_count > 0

    async def delete_post(self, post_id: str) -> bool:
        result = await self.collection.update_one(
            {"post_id": post_id},
            {"$set": {"status": PostStatus.DELETED.value}}
        )
        return result.modified_count > 0

    async def schedule_post(self, post_id: str, scheduled_at: datetime) -> bool:
        return await self.update_post(
            post_id, scheduled_at=scheduled_at,
            status=PostStatus.SCHEDULED.value, is_draft=False
        )

    async def clone_post(self, post_id: str, created_by: int) -> Optional[Dict]:
        original = await self.get_post(post_id)
        if not original:
            return None
        cloned = PostModel(
            title=f"[Clone] {original.get('title', '')}",
            content=original.get("content"),
            media_file_id=original.get("media_file_id"),
            media_type=original.get("media_type"),
            caption=original.get("caption"),
            button_rows=original.get("button_rows", []),
            created_by=created_by, is_draft=True,
        )
        await self.collection.insert_one(cloned.dict())
        await self.collection.update_one({"post_id": post_id}, {"$inc": {"clone_count": 1}})
        return cloned.dict()

    async def get_recent_posts(self, limit: int = 10) -> List[Dict]:
        cursor = self.collection.find(
            {"status": {"$ne": "deleted"}}
        ).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_drafts(self, limit: int = 10) -> List[Dict]:
        cursor = self.collection.find({"is_draft": True}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_total_posts(self) -> int:
        return await self.collection.count_documents({"status": {"$ne": "deleted"}})

    async def get_drafts_count(self) -> int:
        return await self.collection.count_documents({"is_draft": True})

    async def get_scheduled_count(self) -> int:
        return await self.collection.count_documents({"status": "scheduled"})

    async def get_due_scheduled_posts(self) -> List[Dict]:
        now = datetime.utcnow()
        cursor = self.collection.find({
            "status": "scheduled",
            "scheduled_at": {"$lte": now}
        })
        return await cursor.to_list(length=50)

    async def get_overall_analytics(self) -> Dict[str, Any]:
        total = await self.collection.count_documents({"status": {"$ne": "deleted"}})
        published = await self.collection.count_documents({"status": "published"})
        drafts = await self.collection.count_documents({"is_draft": True})
        scheduled = await self.collection.count_documents({"status": "scheduled"})
        week_ago = datetime.utcnow() - timedelta(days=7)
        this_week = await self.collection.count_documents({"created_at": {"$gte": week_ago}})

        pipeline = [{"$group": {"_id": None,
            "total_views": {"$sum": "$views"},
            "total_forwards": {"$sum": "$forwards"},
            "total_reactions": {"$sum": "$reactions"}
        }}]
        agg = await self.collection.aggregate(pipeline).to_list(length=1)
        agg = agg[0] if agg else {}

        return {
            "total": total, "published": published, "drafts": drafts,
            "scheduled": scheduled, "this_week": this_week,
            "total_views": agg.get("total_views", 0),
            "total_forwards": agg.get("total_forwards", 0),
            "total_reactions": agg.get("total_reactions", 0),
        }
