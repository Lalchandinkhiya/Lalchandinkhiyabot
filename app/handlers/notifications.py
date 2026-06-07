"""Notifications Handler - Notification center."""
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.admin_keyboards import get_back_keyboard
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()


@router.callback_query(F.data == "menu_notifications")
async def cb_notifications_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    db = get_db()
    user_id = callback.from_user.id
    unread = await db.notifications.count_documents({"is_read": False, "user_id": user_id})
    total = await db.notifications.count_documents({"user_id": user_id})
    recent = await db.notifications.find(
        {"user_id": user_id}
    ).sort("created_at", -1).limit(5).to_list(5)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Mark All Read", callback_data="notif_mark_read"),
        InlineKeyboardButton(text="🗑️ Clear All", callback_data="notif_clear"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Back", callback_data="admin_dashboard"))

    text = f"""
🔔 <b>NOTIFICATION CENTER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Summary:</b>
🔴 Unread: <code>{unread}</code>
📬 Total: <code>{total}</code>

<b>Recent Notifications:</b>
"""
    if recent:
        icons = {"info": "🔵", "warning": "🟡", "error": "🔴", "success": "🟢"}
        for notif in recent:
            icon = icons.get(notif.get("notif_type", "info"), "🔵")
            read_mark = "" if notif.get("is_read") else " 🔴"
            ts = notif.get("created_at", datetime.utcnow()).strftime("%m/%d %H:%M")
            text += f"\n{icon} <b>{notif.get('title','')}</b>{read_mark}\n   <i>{notif.get('message','')[:50]}</i> [{ts}]\n"
    else:
        text += "\n<i>No notifications yet.</i>"

    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "notif_mark_read")
async def cb_mark_read(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    await db.notifications.update_many(
        {"user_id": callback.from_user.id},
        {"$set": {"is_read": True}}
    )
    await callback.answer("✅ All notifications marked as read!")
    await cb_notifications_menu(callback)


@router.callback_query(F.data == "notif_clear")
async def cb_clear_notifications(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    await db.notifications.delete_many({"user_id": callback.from_user.id})
    await callback.answer("🗑️ All notifications cleared!")
    await cb_notifications_menu(callback)
