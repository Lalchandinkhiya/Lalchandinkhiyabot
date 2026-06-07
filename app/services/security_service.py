"""
Security Service Module
Handles security logging, session management, and authentication.
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from config.database import get_db
from config.settings import settings
from app.models.models import SecurityLogModel, SessionModel, SecurityEventType

logger = logging.getLogger(__name__)


class SecurityService:
    """Service for security features and audit logging."""

    def __init__(self):
        self.db = get_db()

    async def log_event(
        self,
        user_id: int,
        event_type: str,
        description: str,
        ip_address: Optional[str] = None,
        severity: str = "info",
        extra_data: Optional[Dict] = None,
    ) -> None:
        """Log a security event to the database."""
        try:
            log = SecurityLogModel(
                user_id=user_id,
                event_type=SecurityEventType(event_type) if event_type in [e.value for e in SecurityEventType] else SecurityEventType.COMMAND,
                description=description,
                ip_address=ip_address,
                severity=severity,
                extra_data=extra_data or {},
            )
            await self.db.security_logs.insert_one(log.dict())
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")

    async def get_audit_logs(self, limit: int = 20, severity: Optional[str] = None) -> List[Dict]:
        query = {}
        if severity:
            query["severity"] = severity
        cursor = self.db.security_logs.find(query).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_recent_ip_logs(self, limit: int = 20) -> List[Dict]:
        cursor = self.db.security_logs.find(
            {"ip_address": {"$ne": None}}
        ).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_active_sessions(self) -> List[Dict]:
        now = datetime.utcnow()
        cursor = self.db.sessions.find({
            "expires_at": {"$gt": now},
            "is_active": True
        })
        return await cursor.to_list(length=50)

    async def create_session(self, user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        session = SessionModel(
            user_id=user_id,
            session_token=token,
            expires_at=datetime.utcnow() + timedelta(seconds=settings.SESSION_TIMEOUT),
        )
        await self.db.sessions.replace_one(
            {"user_id": user_id},
            session.dict(),
            upsert=True
        )
        return token

    async def invalidate_session(self, user_id: int) -> None:
        await self.db.sessions.update_one(
            {"user_id": user_id},
            {"$set": {"is_active": False}}
        )

    async def kill_all_sessions(self) -> int:
        result = await self.db.sessions.update_many(
            {}, {"$set": {"is_active": False}}
        )
        return result.modified_count

    async def get_all_admins(self) -> List[Dict]:
        cursor = self.db.users.find({
            "role": {"$in": ["admin", "super_admin"]}
        })
        return await cursor.to_list(length=50)

    async def get_blacklist(self, limit: int = 20) -> List[Dict]:
        cursor = self.db.blacklist.find({}).sort("banned_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_blacklist_count(self) -> int:
        return await self.db.blacklist.count_documents({})

    async def get_unverified_channels(self) -> List[Dict]:
        cursor = self.db.channels.find({"is_verified": False})
        return await cursor.to_list(length=20)

    async def check_failed_auth_attempts(self, user_id: int) -> int:
        cutoff = datetime.utcnow() - timedelta(hours=1)
        return await self.db.security_logs.count_documents({
            "user_id": user_id,
            "event_type": "failed_auth",
            "timestamp": {"$gte": cutoff}
        })
