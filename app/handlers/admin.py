"""Admin Handler - Broadcast, maintenance, settings, multi-admin."""
import asyncio
import logging
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.keyboards.admin_keyboards import get_back_keyboard, get_admin_dashboard_keyboard
from app.services.user_service import UserService
from app.services.security_service import SecurityService
from app.utils.helpers import is_admin
from config.settings import settings
from config.database import get_db

router = Router()
logger = logging.getLogger(__name__)


class AdminStates(StatesGroup):
    waiting_broadcast_msg = State()
    waiting_maintenance_msg = State()
    waiting_add_admin_id = State()
    waiting_welcome_msg = State()


# ── Broadcast ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "broadcast_start")
async def cb_broadcast_start(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await state.set_state(AdminStates.waiting_broadcast_msg)
    await callback.message.edit_text(
        "📤 <b>BROADCAST MESSAGE</b>\n"
        "<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
        "Send the message to broadcast to <b>ALL users</b>.\n\n"
        "✅ Supports: Text, Photos, Videos, Documents\n"
        "✅ HTML formatting supported\n"
        "✅ Inline buttons supported\n\n"
        "⚠️ This will be sent to all registered users!\n\n"
        "/cancel - Cancel broadcast",
        reply_markup=get_back_keyboard("admin_dashboard")
    )
    await callback.answer()


@router.message(AdminStates.waiting_broadcast_msg)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.text == "/cancel":
        await state.clear()
        await message.answer("❌ Broadcast cancelled.")
        return

    await state.clear()
    svc = UserService()
    user_ids = await svc.get_all_active_user_ids()
    total = len(user_ids)

    if total == 0:
        await message.answer("⚠️ No active users found.")
        return

    progress_msg = await message.answer(
        f"📤 <b>Broadcasting...</b>\n"
        f"👥 Total: <code>{total}</code>\n"
        f"✅ Sent: <code>0</code>\n"
        f"❌ Failed: <code>0</code>"
    )

    db = get_db()
    from app.models.models import BroadcastModel, BroadcastStatus
    broadcast = BroadcastModel(
        message_content=message.text or message.caption or "",
        started_by=message.from_user.id,
        total_users=total,
        status=BroadcastStatus.RUNNING,
        started_at=datetime.utcnow(),
    )
    await db.broadcasts.insert_one(broadcast.dict())

    sent = 0
    failed = 0
    blocked = 0

    for i, uid in enumerate(user_ids):
        try:
            if message.photo:
                await bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(uid, message.video.file_id, caption=message.caption)
            elif message.document:
                await bot.send_document(uid, message.document.file_id, caption=message.caption)
            else:
                await bot.send_message(uid, message.text)
            sent += 1
        except Exception as e:
            err = str(e).lower()
            if "blocked" in err or "deactivated" in err:
                blocked += 1
            else:
                failed += 1

        # Update progress every 20 users
        if (i + 1) % 20 == 0:
            try:
                pct = round(((i + 1) / total) * 100)
                await progress_msg.edit_text(
                    f"📤 <b>Broadcasting...</b> {pct}%\n"
                    f"👥 Total: <code>{total}</code>\n"
                    f"✅ Sent: <code>{sent}</code>\n"
                    f"❌ Failed: <code>{failed}</code>\n"
                    f"🚫 Blocked: <code>{blocked}</code>"
                )
            except Exception:
                pass
        await asyncio.sleep(0.05)  # Rate limit protection

    # Update broadcast record
    await db.broadcasts.update_one(
        {"broadcast_id": broadcast.broadcast_id},
        {"$set": {
            "status": BroadcastStatus.COMPLETED.value,
            "sent_count": sent, "failed_count": failed,
            "blocked_count": blocked, "progress_pct": 100.0,
            "completed_at": datetime.utcnow(),
        }}
    )

    await progress_msg.edit_text(
        f"✅ <b>Broadcast Complete!</b>\n"
        f"<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
        f"👥 Total Users: <code>{total}</code>\n"
        f"✅ Successfully Sent: <code>{sent}</code>\n"
        f"❌ Failed: <code>{failed}</code>\n"
        f"🚫 Bot Blocked: <code>{blocked}</code>\n"
        f"📊 Success Rate: <code>{round(sent/total*100 if total else 0, 1)}%</code>",
        reply_markup=get_admin_dashboard_keyboard()
    )


# ── Maintenance Mode ───────────────────────────────────────────────────────

@router.message(Command("maintenance"))
async def cmd_maintenance(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    current = settings.MAINTENANCE_MODE
    settings.MAINTENANCE_MODE = not current
    status = "🔧 ENABLED" if settings.MAINTENANCE_MODE else "✅ DISABLED"
    await message.answer(
        f"🔧 <b>Maintenance Mode: {status}</b>\n\n"
        f"<i>{'Users are now blocked from using the bot.' if settings.MAINTENANCE_MODE else 'Users can now use the bot normally.'}</i>"
    )
    sec = SecurityService()
    await sec.log_event(
        message.from_user.id, "admin_action",
        f"Maintenance mode {'enabled' if settings.MAINTENANCE_MODE else 'disabled'}"
    )


# ── Add Admin ──────────────────────────────────────────────────────────────

@router.message(Command("addadmin"))
async def cmd_add_admin(message: Message, state: FSMContext) -> None:
    if message.from_user.id != settings.SUPER_ADMIN_ID:
        await message.answer("⛔ Only the super admin can add admins!")
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: /addadmin <user_id>")
        return

    try:
        new_admin_id = int(parts[1])
        svc = UserService()
        from app.models.models import UserRole
        success = await svc.promote_to_admin(new_admin_id, UserRole.ADMIN)
        if success:
            if new_admin_id not in settings.ADMIN_IDS:
                settings.ADMIN_IDS.append(new_admin_id)
            await message.answer(f"✅ User <code>{new_admin_id}</code> promoted to admin!")
            sec = SecurityService()
            await sec.log_event(
                message.from_user.id, "admin_action",
                f"Promoted user {new_admin_id} to admin"
            )
        else:
            await message.answer(f"⚠️ User {new_admin_id} not found in database.")
    except ValueError:
        await message.answer("❌ Invalid user ID.")


# ── Stats Command ──────────────────────────────────────────────────────────

@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    from app.services.stats_service import StatsService
    stats = StatsService()
    data = await stats.get_dashboard_stats()
    await message.answer(
        f"📊 <b>Quick Stats</b>\n\n"
        f"👥 Users: <code>{data['total_users']}</code>\n"
        f"🟢 Active: <code>{data['active_users']}</code>\n"
        f"📝 Posts: <code>{data['total_posts']}</code>\n"
        f"📢 Channels: <code>{data['total_channels']}</code>\n"
        f"🗃️ DB: <code>{'✅ OK' if data['db_healthy'] else '❌ Error'}</code>"
    )


# ── Settings Menu ──────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_settings")
async def cb_settings_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔧 Maintenance Mode", callback_data="toggle_maintenance"),
        InlineKeyboardButton(text="📌 Force Subscribe", callback_data="toggle_forcesub"),
    )
    builder.row(
        InlineKeyboardButton(text="💬 Welcome Message", callback_data="user_welcome"),
        InlineKeyboardButton(text="🤖 Bot Info", callback_data="bot_info"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Back", callback_data="admin_dashboard"))

    text = f"""
⚙️ <b>BOT SETTINGS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

🔧 Maintenance: <code>{'ON ⚠️' if settings.MAINTENANCE_MODE else 'OFF ✅'}</code>
📌 Force Subscribe: <code>{'ON ✅' if settings.FORCE_SUBSCRIBE else 'OFF ❌'}</code>
📢 Force Sub Channel: <code>{settings.FORCE_SUBSCRIBE_CHANNEL or 'Not set'}</code>
🌐 Bot Version: <code>v2.0.0</code>
"""
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "toggle_maintenance")
async def cb_toggle_maintenance(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    settings.MAINTENANCE_MODE = not settings.MAINTENANCE_MODE
    status = "ENABLED ⚠️" if settings.MAINTENANCE_MODE else "DISABLED ✅"
    await callback.answer(f"🔧 Maintenance mode {status}", show_alert=True)
    await cb_settings_menu(callback)


@router.callback_query(F.data == "bot_info")
async def cb_bot_info(callback: CallbackQuery, bot: Bot) -> None:
    me = await bot.get_me()
    text = f"""
🤖 <b>BOT INFORMATION</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

🤖 Name: <b>{me.full_name}</b>
👤 Username: @{me.username}
🆔 Bot ID: <code>{me.id}</code>
🔱 Version: <code>v2.0.0</code>
⚡ Framework: <code>Aiogram 3.x</code>
🗃️ Database: <code>MongoDB</code>
🐍 Language: <code>Python 3.11+</code>
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_settings"))
    await callback.answer()
