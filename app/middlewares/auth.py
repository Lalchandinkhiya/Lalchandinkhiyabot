"""
Authentication Middleware
Validates admin access and manages sessions.
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from config.settings import settings
from app.services.user_service import UserService
from app.services.security_service import SecurityService

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """
    Authentication middleware.
    - Updates user's last activity
    - Logs admin commands
    - Checks for banned users
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = None

        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user:
            user_service = UserService()

            # Check if user is banned
            is_banned = await user_service.is_banned(user.id)
            if is_banned:
                if isinstance(event, Message):
                    await event.answer("🚫 You have been banned from using this bot.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("🚫 You are banned!", show_alert=True)
                return

            # Update last activity
            await user_service.update_activity(user.id)

            # Store user info in data for handlers
            data["user_id"] = user.id
            data["is_admin"] = user.id in settings.ADMIN_IDS or user.id == settings.SUPER_ADMIN_ID

        return await handler(event, data)
