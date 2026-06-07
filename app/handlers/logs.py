"""Logs Handler - Error monitoring and log viewer."""
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from app.keyboards.admin_keyboards import get_logs_keyboard, get_back_keyboard
from app.services.security_service import SecurityService
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()


@router.callback_query(F.data == "menu_logs")
async def cb_logs_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    total = await db.security_logs.count_documents({})
    errors = await db.security_logs.count_documents({"severity": "critical"})
    warnings = await db.security_logs.count_documents({"severity": "warning"})
    text = f"""
📋 <b>LOGS VIEWER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Log Statistics:</b>
📝 Total Logs: <code>{total}</code>
❌ Critical: <code>{errors}</code>
⚠️ Warnings: <code>{warnings}</code>
ℹ️ Info: <code>{total - errors - warnings}</code>

<i>Logs auto-delete after 90 days.</i>
"""
    await callback.message.edit_text(text, reply_markup=get_logs_keyboard())
    await callback.answer()


@router.callback_query(F.data == "log_all")
async def cb_log_all(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    sec = SecurityService()
    logs = await sec.get_audit_logs(limit=10)
    text = "📋 <b>RECENT LOGS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    icons = {"info": "🔵", "warning": "🟡", "critical": "🔴"}
    for log in logs:
        icon = icons.get(log.get("severity", "info"), "🔵")
        ts = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
        text += f"{icon} <code>{ts}</code> | {log.get('description','')[:45]}\n"
    if not logs:
        text += "<i>No logs found.</i>"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_logs"))
    await callback.answer()


@router.callback_query(F.data == "log_errors")
async def cb_log_errors(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    sec = SecurityService()
    logs = await sec.get_audit_logs(limit=10, severity="critical")
    text = "❌ <b>CRITICAL ERROR LOGS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    for log in logs:
        ts = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
        text += f"🔴 <code>{ts}</code> | UID:{log.get('user_id','?')} | {log.get('description','')[:40]}\n"
    if not logs:
        text += "<i>✅ No critical errors found.</i>"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_logs"))
    await callback.answer()


@router.callback_query(F.data == "log_security")
async def cb_log_security(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    logs = await db.security_logs.find(
        {"event_type": {"$in": ["ban", "flood", "failed_auth", "suspicious"]}}
    ).sort("timestamp", -1).limit(10).to_list(10)
    text = "🛡️ <b>SECURITY LOGS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    for log in logs:
        ts = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
        etype = log.get("event_type", "?").upper()
        text += f"🛡️ <code>{ts}</code> | <b>{etype}</b> | UID:{log.get('user_id','?')}\n   <i>{log.get('description','')[:40]}</i>\n"
    if not logs:
        text += "<i>No security events found.</i>"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_logs"))
    await callback.answer()


@router.callback_query(F.data == "log_clear")
async def cb_clear_logs(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    from app.keyboards.admin_keyboards import get_confirmation_keyboard
    await callback.message.edit_text(
        "⚠️ <b>Clear All Logs?</b>\n\nThis will delete all security logs permanently!",
        reply_markup=get_confirmation_keyboard("log_clear_confirm", "menu_logs")
    )
    await callback.answer()


@router.callback_query(F.data == "log_clear_confirm")
async def cb_clear_logs_confirm(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    result = await db.security_logs.delete_many({})
    await callback.answer(f"🗑️ Deleted {result.deleted_count} log entries!", show_alert=True)
    await cb_logs_menu(callback)


@router.message(Command("logs"))
async def cmd_logs(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    sec = SecurityService()
    logs = await sec.get_audit_logs(limit=5)
    text = "📋 <b>Recent Logs:</b>\n\n"
    for log in logs:
        ts = log.get("timestamp", datetime.utcnow()).strftime("%m/%d %H:%M")
        text += f"• <code>{ts}</code> - {log.get('description','')[:50]}\n"
    await message.answer(text)
