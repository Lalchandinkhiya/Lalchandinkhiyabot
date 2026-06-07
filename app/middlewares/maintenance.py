"""
Maintenance Middleware
Blocks all non-admin access during maintenance mode.
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from config.settings import settings
from app.utils.helpers import is_admin

logger = logging.getLogger(__name__)


class MaintenanceMiddleware(BaseMiddleware):
    """Blocks users during maintenance mode."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not settings.MAINTENANCE_MODE:
            return await handler(event, data)

        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user and is_admin(user.id):
            return await handler(event, data)

        # Block non-admins during maintenance
        if isinstance(event, Message):
            await event.answer(
                "🔧 <b>Bot is under maintenance!</b>\n\n"
                "We'll be back shortly. Please try again later."
            )
        elif isinstance(event, CallbackQuery):
            await event.answer("🔧 Bot under maintenance!", show_alert=True)

        return  # Block the update
