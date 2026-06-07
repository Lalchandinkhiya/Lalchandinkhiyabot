"""
╔══════════════════════════════════════════════════════════════╗
║           LALCHAND INKHIYA - TELEGRAM BOT                   ║
║           Production-Ready | MongoDB | Aiogram 3.x           ║
╚══════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from config.database import init_db, close_db
from app.handlers import start, admin, posts, captions, links
from app.handlers import buttons, advertisements, security, users
from app.handlers import channels, media, backup, notifications, logs
from app.middlewares.auth import AuthMiddleware
from app.middlewares.anti_spam import AntiSpamMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.maintenance import MaintenanceMiddleware
from app.utils.logger import setup_logger, get_logger
from app.utils.startup_banner import print_startup_banner

logger = get_logger(__name__)


async def on_startup(bot: Bot) -> None:
    logger.info("🚀 Bot starting up...")
    await init_db()
    logger.info("✅ Database connected")

    from app.utils.bot_commands import set_bot_commands
    await set_bot_commands(bot)

    from app.services.notification_service import notify_admins_startup
    await notify_admins_startup(bot)
    logger.info("✅ Bot startup complete!")


async def on_shutdown(bot: Bot) -> None:
    logger.info("🛑 Bot shutting down...")
    try:
        from app.services.notification_service import notify_admins_shutdown
        await notify_admins_shutdown(bot)
    except Exception:
        pass
    await close_db()
    logger.info("👋 Bot stopped")


async def main() -> None:
    print_startup_banner()
    setup_logger()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        )
    )

    # Using MemoryStorage by default (works without extra packages)
    # For production with persistence, install motor and use MongoStorage
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # ── Middlewares ───────────────────────────────────────────────
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(MaintenanceMiddleware())
    dp.message.middleware(AntiSpamMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.callback_query.middleware(MaintenanceMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    # ── Routers ───────────────────────────────────────────────────
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(posts.router)
    dp.include_router(captions.router)
    dp.include_router(links.router)
    dp.include_router(buttons.router)
    dp.include_router(advertisements.router)
    dp.include_router(security.router)
    dp.include_router(users.router)
    dp.include_router(channels.router)
    dp.include_router(media.router)
    dp.include_router(backup.router)
    dp.include_router(notifications.router)
    dp.include_router(logs.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    me = await bot.get_me()
    logger.info(f"🤖 Starting bot: @{me.username}")

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
