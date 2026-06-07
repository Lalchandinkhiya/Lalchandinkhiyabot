"""Bot Commands - Register bot command menu."""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from config.settings import settings


async def set_bot_commands(bot: Bot) -> None:
    """Set bot command list visible in Telegram."""
    # Default commands for all users
    user_commands = [
        BotCommand(command="start", description="🚀 Start the bot"),
        BotCommand(command="help", description="❓ Get help"),
    ]

    # Admin commands
    admin_commands = [
        BotCommand(command="start", description="🔱 Open Admin Dashboard"),
        BotCommand(command="stats", description="📊 Quick Statistics"),
        BotCommand(command="broadcast", description="📤 Broadcast Message"),
        BotCommand(command="ban", description="🚫 Ban a user"),
        BotCommand(command="unban", description="✅ Unban a user"),
        BotCommand(command="addadmin", description="👑 Add new admin (Super Admin only)"),
        BotCommand(command="maintenance", description="🔧 Toggle maintenance mode"),
        BotCommand(command="backup", description="💾 Create database backup"),
        BotCommand(command="logs", description="📋 View recent logs"),
        BotCommand(command="help", description="❓ Show help"),
    ]

    # Set default commands
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    # Set admin-specific commands
    admin_ids = list(set(settings.ADMIN_IDS + [settings.SUPER_ADMIN_ID]))
    for admin_id in admin_ids:
        try:
            await bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except Exception:
            pass
