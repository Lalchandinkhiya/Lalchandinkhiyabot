"""
Database Configuration Module
MongoDB connection management and collection initialization.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, IndexModel
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from config.settings import settings

logger = logging.getLogger(__name__)

# Global database client and database references
_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None


def get_db() -> AsyncIOMotorDatabase:
    """Get the database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


async def init_db() -> None:
    """Initialize MongoDB connection and create indexes."""
    global _client, _db

    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
        )

        # Test connection
        await _client.admin.command('ping')
        _db = _client[settings.DB_NAME]

        # Create all collections and indexes
        await _create_indexes()

        logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.critical(f"❌ MongoDB connection failed: {e}")
        raise


async def close_db() -> None:
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB connection closed")


async def _create_indexes() -> None:
    """Create all necessary database indexes for performance."""
    db = _db

    # ── Users Collection ──────────────────────────────────────────
    await db.users.create_indexes([
        IndexModel([("user_id", ASCENDING)], unique=True),
        IndexModel([("username", ASCENDING)]),
        IndexModel([("is_active", ASCENDING)]),
        IndexModel([("joined_at", DESCENDING)]),
        IndexModel([("is_banned", ASCENDING)]),
        IndexModel([("last_activity", DESCENDING)]),
    ])

    # ── Posts Collection ──────────────────────────────────────────
    await db.posts.create_indexes([
        IndexModel([("post_id", ASCENDING)], unique=True),
        IndexModel([("created_by", ASCENDING)]),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("scheduled_at", ASCENDING)]),
        IndexModel([("is_draft", ASCENDING)]),
    ])

    # ── Channels Collection ───────────────────────────────────────
    await db.channels.create_indexes([
        IndexModel([("channel_id", ASCENDING)], unique=True),
        IndexModel([("is_active", ASCENDING)]),
        IndexModel([("added_at", DESCENDING)]),
    ])

    # ── Advertisements Collection ─────────────────────────────────
    await db.advertisements.create_indexes([
        IndexModel([("ad_id", ASCENDING)], unique=True),
        IndexModel([("is_active", ASCENDING)]),
        IndexModel([("priority", DESCENDING)]),
        IndexModel([("ad_type", ASCENDING)]),
        IndexModel([("expires_at", ASCENDING)]),
    ])

    # ── Security Logs Collection ──────────────────────────────────
    await db.security_logs.create_indexes([
        IndexModel([("user_id", ASCENDING)]),
        IndexModel([("event_type", ASCENDING)]),
        IndexModel([("timestamp", DESCENDING)]),
        IndexModel([("ip_address", ASCENDING)]),
        # TTL: auto-delete logs older than 90 days
        IndexModel([("timestamp", ASCENDING)], expireAfterSeconds=7776000),
    ])

    # ── Sessions Collection ───────────────────────────────────────
    await db.sessions.create_indexes([
        IndexModel([("user_id", ASCENDING)], unique=True),
        IndexModel([("session_token", ASCENDING)], unique=True),
        # TTL: auto-expire sessions
        IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0),
    ])

    # ── Broadcasts Collection ─────────────────────────────────────
    await db.broadcasts.create_indexes([
        IndexModel([("broadcast_id", ASCENDING)], unique=True),
        IndexModel([("status", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        IndexModel([("started_by", ASCENDING)]),
    ])

    # ── Captions Collection ───────────────────────────────────────
    await db.captions.create_indexes([
        IndexModel([("caption_id", ASCENDING)], unique=True),
        IndexModel([("created_by", ASCENDING)]),
        IndexModel([("name", ASCENDING)]),
    ])

    # ── Links Collection ──────────────────────────────────────────
    await db.links.create_indexes([
        IndexModel([("original_url", ASCENDING)]),
        IndexModel([("short_url", ASCENDING)], unique=True, sparse=True),
        IndexModel([("click_count", DESCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
    ])

    # ── Media Library Collection ──────────────────────────────────
    await db.media_library.create_indexes([
        IndexModel([("file_id", ASCENDING)], unique=True),
        IndexModel([("media_type", ASCENDING)]),
        IndexModel([("uploaded_by", ASCENDING)]),
        IndexModel([("tags", ASCENDING)]),
        IndexModel([("uploaded_at", DESCENDING)]),
    ])

    # ── Button Templates Collection ───────────────────────────────
    await db.button_templates.create_indexes([
        IndexModel([("template_id", ASCENDING)], unique=True),
        IndexModel([("created_by", ASCENDING)]),
        IndexModel([("name", ASCENDING)]),
    ])

    # ── Blacklist Collection ──────────────────────────────────────
    await db.blacklist.create_indexes([
        IndexModel([("user_id", ASCENDING)], unique=True),
        IndexModel([("banned_at", DESCENDING)]),
    ])

    # ── Settings Collection ───────────────────────────────────────
    await db.bot_settings.create_indexes([
        IndexModel([("key", ASCENDING)], unique=True),
    ])

    # ── Notifications Collection ──────────────────────────────────
    await db.notifications.create_indexes([
        IndexModel([("user_id", ASCENDING)]),
        IndexModel([("is_read", ASCENDING)]),
        IndexModel([("created_at", DESCENDING)]),
        # TTL: auto-delete after 30 days
        IndexModel([("created_at", ASCENDING)], expireAfterSeconds=2592000),
    ])

    logger.info("✅ All database indexes created")


async def check_db_health() -> dict:
    """Check database health and return status info."""
    try:
        await _client.admin.command('ping')
        stats = await _db.command("dbStats")
        return {
            "status": "healthy",
            "collections": stats.get("collections", 0),
            "data_size_mb": round(stats.get("dataSize", 0) / 1024 / 1024, 2),
            "storage_size_mb": round(stats.get("storageSize", 0) / 1024 / 1024, 2),
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
