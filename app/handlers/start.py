"""
Start Handler Module
Handles /start command and main admin dashboard display.
"""

from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.services.user_service import UserService
from app.services.stats_service import StatsService
from app.keyboards.admin_keyboards import (
    get_main_menu_keyboard,
    get_admin_dashboard_keyboard,
)
from app.utils.helpers import is_admin, format_uptime, format_number
from config.settings import settings

router = Router()
logger = logging.getLogger(__name__)

BOT_START_TIME = datetime.now(timezone.utc)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command - show welcome or admin dashboard."""
    user = message.from_user
    user_service = UserService()

    # Register/update user
    await user_service.register_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
    )

    if is_admin(user.id):
        await show_admin_dashboard(message)
    else:
        await show_user_welcome(message)


async def show_admin_dashboard(message: Message) -> None:
    """Display the premium admin dashboard."""
    stats = StatsService()
    data = await stats.get_dashboard_stats()
    uptime = format_uptime(BOT_START_TIME)

    dashboard_text = f"""
╔══════════════════════════════════════╗
║  <b>🔱 LALCHAND INKHIYA BOT 🔱</b>         ║
║  <i>Premium Admin Control Panel</i>        ║
╚══════════════════════════════════════╝

<b>👑 Welcome back, Admin!</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>📊 LIVE STATISTICS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
👥 <b>Total Users:</b>     <code>{format_number(data['total_users'])}</code>
🟢 <b>Active Users:</b>    <code>{format_number(data['active_users'])}</code>
📝 <b>Total Posts:</b>     <code>{format_number(data['total_posts'])}</code>
📢 <b>Channels:</b>        <code>{format_number(data['total_channels'])}</code>
📤 <b>Broadcasts:</b>      <code>{format_number(data['total_broadcasts'])}</code>
🚫 <b>Banned Users:</b>    <code>{format_number(data['banned_users'])}</code>

<b>⚙️ SYSTEM STATUS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
⏱️ <b>Uptime:</b>          <code>{uptime}</code>
🗃️ <b>Database:</b>        <code>{'✅ Online' if data['db_healthy'] else '❌ Offline'}</code>
🔧 <b>Maintenance:</b>     <code>{'⚠️ ON' if data['maintenance_mode'] else '✅ OFF'}</code>
🌐 <b>Bot Version:</b>     <code>v2.0.0</code>

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
<i>🕐 Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</i>
"""

    await message.answer(
        text=dashboard_text,
        reply_markup=get_admin_dashboard_keyboard(),
    )


async def show_user_welcome(message: Message) -> None:
    """Display welcome message for regular users."""
    user = message.from_user
    welcome_text = f"""
🌟 <b>Welcome to Lalchand Inkhiya Bot!</b>

Hello, <b>{user.first_name}</b>! 👋

I'm your premium content management assistant.

<i>Use the menu below to get started.</i>
"""
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard(),
    )


@router.callback_query(F.data == "admin_dashboard")
async def cb_admin_dashboard(callback: CallbackQuery) -> None:
    """Refresh admin dashboard."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    stats = StatsService()
    data = await stats.get_dashboard_stats()
    uptime = format_uptime(BOT_START_TIME)

    dashboard_text = f"""
╔══════════════════════════════════════╗
║  <b>🔱 LALCHAND INKHIYA BOT 🔱</b>         ║
║  <i>Premium Admin Control Panel</i>        ║
╚══════════════════════════════════════╝

<b>👑 Admin Dashboard</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>📊 LIVE STATISTICS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
👥 <b>Total Users:</b>     <code>{format_number(data['total_users'])}</code>
🟢 <b>Active Users:</b>    <code>{format_number(data['active_users'])}</code>
📝 <b>Total Posts:</b>     <code>{format_number(data['total_posts'])}</code>
📢 <b>Channels:</b>        <code>{format_number(data['total_channels'])}</code>
📤 <b>Broadcasts:</b>      <code>{format_number(data['total_broadcasts'])}</code>
🚫 <b>Banned Users:</b>    <code>{format_number(data['banned_users'])}</code>

<b>⚙️ SYSTEM STATUS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
⏱️ <b>Uptime:</b>          <code>{uptime}</code>
🗃️ <b>Database:</b>        <code>{'✅ Online' if data['db_healthy'] else '❌ Offline'}</code>
🔧 <b>Maintenance:</b>     <code>{'⚠️ ON' if data['maintenance_mode'] else '✅ OFF'}</code>

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
<i>🕐 Refreshed: {datetime.utcnow().strftime('%H:%M:%S')} UTC</i>
"""

    await callback.message.edit_text(
        text=dashboard_text,
        reply_markup=get_admin_dashboard_keyboard(),
    )
    await callback.answer("✅ Dashboard refreshed!")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Show help information."""
    if is_admin(message.from_user.id):
        help_text = """
<b>🔱 LALCHAND INKHIYA BOT - Admin Help</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>🎛️ Admin Commands:</b>
/start - Open admin dashboard
/stats - Quick statistics
/broadcast - Send broadcast
/addadmin - Add new admin
/ban - Ban a user
/unban - Unban a user
/maintenance - Toggle maintenance mode
/backup - Create database backup
/logs - View recent logs
/help - Show this help

<b>📋 Features:</b>
• Post Management & Scheduling
• Multi-channel Broadcasting
• Auto Caption & Footer
• Link Shortener & Tracker
• Inline Button Creator
• Advertisement Manager
• Security & Audit Logs
• Media Library
• Backup & Restore
"""
    else:
        help_text = """
<b>🌟 Welcome! Here's how to use this bot:</b>

/start - Start the bot
/help - Show this help

Contact an admin for more assistance.
"""

    await message.answer(help_text)
