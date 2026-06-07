"""
User Service Module
Handles all user-related database operations.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from config.database import get_db
from app.models.models import UserModel, UserRole

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users in the database."""

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.users

    async def register_user(
        self,
        user_id: int,
        username: Optional[str],
        first_name: str,
        last_name: Optional[str] = None,
        language_code: Optional[str] = "en",
    ) -> Dict[str, Any]:
        """Register a new user or update existing."""
        full_name = f"{first_name} {last_name or ''}".strip()

        existing = await self.collection.find_one({"user_id": user_id})
        if existing:
            # Update existing user info
            await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "full_name": full_name,
                    "language_code": language_code,
                    "last_activity": datetime.utcnow(),
                    "is_active": True,
                }, "$inc": {"total_messages": 1}}
            )
            return existing

        # Create new user
        user = UserModel(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            language_code=language_code,
        )
        await self.collection.insert_one(user.dict())
        logger.info(f"New user registered: {user_id} (@{username})")
        return user.dict()

    async def get_user(self, user_id: int) -> Optional[Dict]:
        return await self.collection.find_one({"user_id": user_id})

    async def is_banned(self, user_id: int) -> bool:
        user = await self.collection.find_one(
            {"user_id": user_id, "is_banned": True}
        )
        return user is not None

    async def ban_user(self, user_id: int, reason: str, banned_by: int) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "is_banned": True,
                "ban_reason": reason,
                "banned_by": banned_by,
                "banned_at": datetime.utcnow(),
            }}
        )
        # Also add to blacklist collection
        await self.db.blacklist.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "ban_reason": reason,
                "banned_by": banned_by,
                "banned_at": datetime.utcnow(),
            }},
            upsert=True
        )
        return result.modified_count > 0

    async def unban_user(self, user_id: int) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_banned": False, "ban_reason": None}}
        )
        await self.db.blacklist.delete_one({"user_id": user_id})
        return result.modified_count > 0

    async def update_activity(self, user_id: int) -> None:
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity": datetime.utcnow(), "is_active": True},
             "$inc": {"total_messages": 1}}
        )

    async def promote_to_admin(self, user_id: int, role: UserRole = UserRole.ADMIN) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"role": role.value}}
        )
        return result.modified_count > 0

    async def demote_to_user(self, user_id: int) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"role": UserRole.USER.value}}
        )
        return result.modified_count > 0

    async def get_all_users(self, skip: int = 0, limit: int = 50) -> List[Dict]:
        cursor = self.collection.find({}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_total_users(self) -> int:
        return await self.collection.count_documents({})

    async def get_active_users(self, days: int = 7) -> int:
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        return await self.collection.count_documents({
            "last_activity": {"$gte": cutoff},
            "is_banned": {"$ne": True}
        })

    async def get_banned_users_count(self) -> int:
        return await self.collection.count_documents({"is_banned": True})

    async def get_all_active_user_ids(self) -> List[int]:
        cursor = self.collection.find(
            {"is_banned": {"$ne": True}, "is_active": True},
            {"user_id": 1}
        )
        users = await cursor.to_list(length=None)
        return [u["user_id"] for u in users]

    async def search_user(self, query: str) -> List[Dict]:
        cursor = self.collection.find({
            "$or": [
                {"username": {"$regex": query, "$options": "i"}},
                {"full_name": {"$regex": query, "$options": "i"}},
            ]
        }).limit(10)
        return await cursor.to_list(length=10)
