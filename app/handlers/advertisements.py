"""Advertisements Handler - Full ad management system."""
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.admin_keyboards import get_ads_manager_keyboard, get_back_keyboard
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()


@router.callback_query(F.data == "menu_ads")
async def cb_ads_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    total = await db.advertisements.count_documents({})
    active = await db.advertisements.count_documents({"is_active": True})
    text = f"""
📣 <b>ADVERTISEMENT MANAGER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Ad Statistics:</b>
📣 Total Ads: <code>{total}</code>
✅ Active Ads: <code>{active}</code>
⏸️ Paused: <code>{total - active}</code>

<b>Ad Types Available:</b>
🖼️ <b>Banner Ads</b> - Image with caption
📝 <b>Text Ads</b> - Text-only advertisements
⏰ <b>Scheduled Ads</b> - Time-based delivery
🔄 <b>Rotation System</b> - Auto-rotate ads
⚡ <b>Priority Control</b> - Ad priority 1-10
"""
    await callback.message.edit_text(text, reply_markup=get_ads_manager_keyboard())
    await callback.answer()


@router.callback_query(F.data == "ad_create")
async def cb_create_ad(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await callback.message.edit_text(
        "➕ <b>CREATE ADVERTISEMENT</b>\n\n"
        "Use these commands to create ads:\n\n"
        "<b>Text Ad:</b>\n"
        "<code>/newad text</code>\n\n"
        "<b>Banner Ad:</b>\n"
        "<code>/newad banner</code>\n\n"
        "Then follow the setup wizard.",
        reply_markup=get_back_keyboard("menu_ads")
    )
    await callback.answer()


@router.callback_query(F.data == "ad_list")
async def cb_ad_list(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    ads = await db.advertisements.find({}).sort("priority", -1).limit(10).to_list(10)
    text = "📋 <b>ALL ADVERTISEMENTS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    if not ads:
        text += "<i>No advertisements created yet.</i>"
    else:
        for ad in ads:
            status = "✅" if ad.get("is_active") else "⏸️"
            text += f"{status} <code>{ad['ad_id']}</code> | P:{ad.get('priority',5)} | {ad.get('title','N/A')[:25]}\n"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_ads"))
    await callback.answer()


@router.callback_query(F.data == "ad_rotation")
async def cb_ad_rotation(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    from config.settings import settings
    text = f"""
🔄 <b>AD ROTATION SETTINGS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

⚙️ <b>Current Configuration:</b>
📊 Rotation Interval: Every <code>{settings.AD_ROTATION_INTERVAL}</code> posts
🔄 Rotation Mode: <code>Priority-based</code>
⏱️ Min interval: <code>5 posts</code>
📈 Max ads/day: <code>Unlimited</code>

<b>How it works:</b>
After every {settings.AD_ROTATION_INTERVAL} posts, the next
active ad (by priority) is automatically
injected into the channel.
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_ads"))
    await callback.answer()
