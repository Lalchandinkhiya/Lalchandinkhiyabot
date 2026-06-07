"""
Links Handler - Auto link tools.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.admin_keyboards import get_link_tools_keyboard, get_back_keyboard
from app.utils.helpers import is_admin

router = Router()


@router.callback_query(F.data == "menu_links")
async def cb_links_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    text = """
🔗 <b>AUTO LINK TOOLS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

🔄 <b>Link Replacement</b> - Auto swap links in posts
✂️ <b>URL Shortener</b> - Shorten long URLs (Bitly/TinyURL)
🤝 <b>Referral Links</b> - Auto-insert referral codes
📊 <b>Link Analytics</b> - Track clicks & conversions
🔍 <b>Link Tracking</b> - Monitor individual links

<b>Quick Stats:</b>
🔗 Total Links: <code>0</code>
👆 Total Clicks: <code>0</code>
"""
    await callback.message.edit_text(text, reply_markup=get_link_tools_keyboard())
    await callback.answer()


@router.callback_query(F.data == "link_shorten")
async def cb_link_shorten(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await callback.message.edit_text(
        "✂️ <b>URL SHORTENER</b>\n\n"
        "Send the URL you want to shorten:\n\n"
        "<i>Supports: Bitly, TinyURL, custom shortener</i>",
        reply_markup=get_back_keyboard("menu_links")
    )
    await callback.answer()


@router.callback_query(F.data == "link_analytics")
async def cb_link_analytics(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    text = """
📊 <b>LINK ANALYTICS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📈 <b>All-Time Stats:</b>
🔗 Total Links Tracked: <code>0</code>
👆 Total Clicks: <code>0</code>
👤 Unique Visitors: <code>0</code>
📅 Links This Month: <code>0</code>

<i>No link data available yet.</i>
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_links"))
    await callback.answer()
