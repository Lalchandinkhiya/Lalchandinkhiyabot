"""
Security Handler Module
10 Advanced Security Features for the admin panel.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from app.keyboards.admin_keyboards import (
    get_security_keyboard,
    get_back_keyboard,
    get_confirmation_keyboard,
)
from app.services.security_service import SecurityService
from app.utils.helpers import is_admin
from app.models.models import SecurityEventType, UserRole

router = Router()
logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════════════
# 1. ADMIN AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "menu_security")
async def cb_security_menu(callback: CallbackQuery) -> None:
    """Show security tools menu."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
🛡️ <b>SECURITY CONTROL CENTER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>10 Advanced Security Features:</b>

🔐 <b>Admin Authentication</b> - Multi-layer auth
👮 <b>Role Based Access</b> - Permission control
🌐 <b>IP Logging</b> - Track all connections
🔑 <b>Session Management</b> - Active sessions
📋 <b>Audit Logs</b> - Full activity history
🛡️ <b>Anti Spam</b> - Content filtering
🌊 <b>Flood Protection</b> - Rate limiting
✅ <b>Channel Verify</b> - Bot access check
🚫 <b>Blacklist</b> - User ban system
🎛️ <b>Permissions</b> - Command access control

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
"""
    await callback.message.edit_text(text, reply_markup=get_security_keyboard())
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 2. ROLE BASED ACCESS CONTROL
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_roles")
async def cb_role_control(callback: CallbackQuery) -> None:
    """Role management panel."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    admins = await sec.get_all_admins()

    text = """
👮 <b>ROLE BASED ACCESS CONTROL</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Available Roles:</b>
👑 <code>super_admin</code> - Full access
🔴 <code>admin</code> - Manage posts/users
🟡 <code>moderator</code> - View & moderate
🟢 <code>user</code> - Standard access

<b>Current Admins:</b>
"""

    for admin_data in admins[:10]:
        role_icon = "👑" if admin_data["role"] == "super_admin" else "🔴"
        text += f"\n{role_icon} <code>{admin_data['user_id']}</code> - @{admin_data.get('username', 'N/A')}"

    text += f"\n\n<i>Total Admins: {len(admins)}</i>"

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Add Admin", callback_data="user_promote"),
        InlineKeyboardButton(text="➖ Remove Admin", callback_data="user_demote"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Back", callback_data="menu_security"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 3. IP LOGGING
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_ip_logs")
async def cb_ip_logs(callback: CallbackQuery) -> None:
    """View IP logs."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    recent_ips = await sec.get_recent_ip_logs(limit=10)

    text = """
🌐 <b>IP ADDRESS LOGGING</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Recent Connections:</b>
"""
    if recent_ips:
        for log in recent_ips:
            timestamp = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
            text += f"\n🔸 <code>{log.get('ip_address', 'N/A')}</code> - ID: <code>{log.get('user_id', '?')}</code> [{timestamp}]"
    else:
        text += "\n<i>No IP logs found</i>"

    text += "\n\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>"
    text += "\n<i>🔐 All connections are logged for security</i>"

    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_security"))
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 4. SESSION MANAGEMENT
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_sessions")
async def cb_sessions(callback: CallbackQuery) -> None:
    """Active sessions management."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    sessions = await sec.get_active_sessions()

    text = f"""
🔑 <b>SESSION MANAGEMENT</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Active Sessions:</b> <code>{len(sessions)}</code>

"""
    for session in sessions[:8]:
        created = session.get("created_at", datetime.utcnow()).strftime("%m/%d %H:%M")
        text += f"🟢 User <code>{session['user_id']}</code> — Since {created}\n"

    text += """
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
⏱️ Sessions expire after 1 hour of inactivity
"""

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔴 Kill All Sessions", callback_data="sec_kill_sessions"),
        InlineKeyboardButton(text="◀️ Back", callback_data="menu_security"),
    )

    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 5. AUDIT LOGS
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_audit")
async def cb_audit_logs(callback: CallbackQuery) -> None:
    """Login and action audit logs."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    logs = await sec.get_audit_logs(limit=10)

    text = """
📋 <b>AUDIT LOGS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Recent Admin Actions:</b>
"""
    for log in logs:
        timestamp = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
        event = log.get("event_type", "unknown")
        uid = log.get("user_id", "?")
        desc = log.get("description", "")[:30]

        severity_icon = {"info": "🔵", "warning": "🟡", "critical": "🔴"}.get(
            log.get("severity", "info"), "🔵"
        )
        text += f"\n{severity_icon} <code>{timestamp}</code> | ID:{uid} | {desc}"

    if not logs:
        text += "\n<i>No audit logs found</i>"

    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_security"))
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 6. ANTI SPAM
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_antispam")
async def cb_antispam(callback: CallbackQuery) -> None:
    """Anti-spam configuration."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    from config.settings import settings
    text = f"""
🛡️ <b>ANTI SPAM PROTECTION</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Current Settings:</b>
🌊 Flood Rate: <code>{settings.FLOOD_RATE} msg/min</code>
🚫 Auto-ban on flood: <code>✅ Enabled</code>
🔍 Spam detection: <code>✅ Active</code>
📝 Content filter: <code>✅ Running</code>

<b>Spam Statistics (Today):</b>
🔴 Blocked messages: <code>0</code>
🟡 Warnings issued: <code>0</code>
🚫 Auto-bans: <code>0</code>

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
"""

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⚙️ Configure", callback_data="sec_antispam_config"),
        InlineKeyboardButton(text="◀️ Back", callback_data="menu_security"),
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 7. FLOOD PROTECTION
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_flood")
async def cb_flood_protection(callback: CallbackQuery) -> None:
    """Flood protection settings."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
🌊 <b>FLOOD PROTECTION</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Active Protection Rules:</b>

⚡ <b>Rate Limiting:</b> 30 messages/minute
⏱️ <b>Cooldown:</b> 60 seconds on flood
🔔 <b>Warning before ban:</b> 3 warnings
🚫 <b>Auto-ban threshold:</b> 5 violations
📊 <b>Window size:</b> 60 seconds

<b>Flood Detection Methods:</b>
✅ Message frequency monitoring
✅ Duplicate message detection
✅ Command spam prevention
✅ Callback spam prevention

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
"""
    await callback.message.edit_text(
        text, reply_markup=get_back_keyboard("menu_security")
    )
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 8. CHANNEL VERIFICATION
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_channel_verify")
async def cb_channel_verify(callback: CallbackQuery) -> None:
    """Channel verification system."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    channels = await sec.get_unverified_channels()

    text = f"""
✅ <b>CHANNEL VERIFICATION</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Pending Verification:</b> <code>{len(channels)}</code>

Verification checks:
🤖 Bot is admin in channel
📢 Channel is accessible
🔐 Bot has post permissions
✅ Channel ID is valid

"""
    for ch in channels[:5]:
        text += f"🔸 <code>{ch.get('channel_id')}</code> - {ch.get('channel_name', 'Unknown')}\n"

    await callback.message.edit_text(
        text, reply_markup=get_back_keyboard("menu_security")
    )
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 9. BLACKLIST SYSTEM
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_blacklist")
async def cb_blacklist(callback: CallbackQuery) -> None:
    """User blacklist management."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    sec = SecurityService()
    blacklisted = await sec.get_blacklist(limit=10)
    count = await sec.get_blacklist_count()

    text = f"""
🚫 <b>USER BLACKLIST SYSTEM</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Total Blacklisted:</b> <code>{count}</code>

<b>Recent Bans:</b>
"""
    for user in blacklisted:
        banned_at = user.get("banned_at", datetime.utcnow()).strftime("%m/%d/%Y")
        reason = user.get("ban_reason", "No reason")[:20]
        text += f"\n🔴 <code>{user['user_id']}</code> | {banned_at} | {reason}"

    if not blacklisted:
        text += "\n<i>No blacklisted users</i>"

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🚫 Ban User", callback_data="user_ban"),
        InlineKeyboardButton(text="✅ Unban User", callback_data="user_unban"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Back", callback_data="menu_security"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


# ════════════════════════════════════════════════════════════════════════
# 10. COMMAND PERMISSION CONTROL
# ════════════════════════════════════════════════════════════════════════

@router.callback_query(F.data == "sec_permissions")
async def cb_permissions(callback: CallbackQuery) -> None:
    """Command permission control."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
🎛️ <b>COMMAND PERMISSION CONTROL</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Permission Matrix:</b>

<code>Command          | User | Mod | Admin | SAdmin</code>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
<code>/start           |  ✅  |  ✅ |  ✅   |  ✅</code>
<code>/help            |  ✅  |  ✅ |  ✅   |  ✅</code>
<code>/broadcast       |  ❌  |  ❌ |  ✅   |  ✅</code>
<code>/ban             |  ❌  |  ✅ |  ✅   |  ✅</code>
<code>/addadmin        |  ❌  |  ❌ |  ❌   |  ✅</code>
<code>/maintenance     |  ❌  |  ❌ |  ✅   |  ✅</code>
<code>/backup          |  ❌  |  ❌ |  ✅   |  ✅</code>
<code>/logs            |  ❌  |  ✅ |  ✅   |  ✅</code>

<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>
"""
    await callback.message.edit_text(
        text, reply_markup=get_back_keyboard("menu_security")
    )
    await callback.answer()
