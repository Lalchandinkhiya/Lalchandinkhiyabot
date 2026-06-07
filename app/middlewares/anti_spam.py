"""
Anti-Spam Middleware
Flood protection and spam detection middleware.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from config.settings import settings
from app.utils.helpers import is_admin

logger = logging.getLogger(__name__)


class AntiSpamMiddleware(BaseMiddleware):
    """
    Middleware for flood protection and spam detection.
    
    Features:
    - Rate limiting (N messages per minute)
    - Duplicate message detection
    - Auto-warning system
    - Temporary muting
    """

    def __init__(self):
        self.user_messages: Dict[int, list] = defaultdict(list)
        self.user_warnings: Dict[int, int] = defaultdict(int)
        self.muted_users: Dict[int, datetime] = {}
        self.max_messages = settings.FLOOD_RATE  # per minute
        self.mute_duration = 60  # seconds
        self.max_warnings = 3

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id

        # Admins bypass flood protection
        if is_admin(user_id):
            return await handler(event, data)

        # Check if user is muted
        if user_id in self.muted_users:
            mute_until = self.muted_users[user_id]
            if datetime.utcnow() < mute_until:
                remaining = int((mute_until - datetime.utcnow()).total_seconds())
                await event.answer(
                    f"⚠️ You're sending messages too fast!\n"
                    f"Please wait <b>{remaining}s</b> before sending more.",
                )
                return  # Block the update
            else:
                del self.muted_users[user_id]
                self.user_warnings[user_id] = 0

        # Clean old message timestamps
        now = datetime.utcnow()
        window = now - timedelta(minutes=1)
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id] if t > window
        ]

        # Add current message
        self.user_messages[user_id].append(now)

        # Check flood
        if len(self.user_messages[user_id]) > self.max_messages:
            self.user_warnings[user_id] += 1
            warnings = self.user_warnings[user_id]

            if warnings >= self.max_warnings:
                # Mute user
                self.muted_users[user_id] = now + timedelta(seconds=self.mute_duration)
                logger.warning(f"User {user_id} muted for flooding")
                await event.answer(
                    f"🚫 <b>Flood detected!</b>\n"
                    f"You've been muted for {self.mute_duration} seconds."
                )

                # Log security event
                from app.services.security_service import SecurityService
                sec = SecurityService()
                await sec.log_event(
                    user_id=user_id,
                    event_type="flood",
                    description=f"User muted for {self.mute_duration}s - flood detected",
                    severity="warning"
                )
                return

            else:
                await event.answer(
                    f"⚠️ <b>Slow down!</b> Warning {warnings}/{self.max_warnings}\n"
                    f"Continued flooding will result in a mute."
                )
                return

        return await handler(event, data)
