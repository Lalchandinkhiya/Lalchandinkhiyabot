"""Buttons Handler - Inline button creator and manager."""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.admin_keyboards import get_button_tools_keyboard, get_back_keyboard
from app.utils.helpers import is_admin

router = Router()


@router.callback_query(F.data == "menu_buttons")
async def cb_buttons_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    text = """
🔘 <b>AUTO BUTTON TOOLS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

➕ <b>Create Buttons</b> - Build inline keyboards
📋 <b>Templates</b> - Save button layouts
🔗 <b>URL Buttons</b> - Link to external URLs
⚙️ <b>Callback Buttons</b> - Trigger bot actions
📐 <b>Multi Row</b> - Multiple button rows
🤖 <b>Auto Add</b> - Append buttons to posts

<b>Button Format:</b>
<code>Button Text | https://url.com</code>
<code>Button 1 | url1 || Button 2 | url2</code>

<i>Use || to separate buttons in same row
Use newline for new rows</i>
"""
    await callback.message.edit_text(text, reply_markup=get_button_tools_keyboard())
    await callback.answer()


@router.callback_query(F.data == "btn_create")
async def cb_create_buttons(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await callback.message.edit_text(
        "➕ <b>CREATE INLINE BUTTONS</b>\n\n"
        "Send buttons in format:\n\n"
        "<code>Button Text | https://example.com</code>\n\n"
        "Multiple buttons per row:\n"
        "<code>Btn 1 | url1 || Btn 2 | url2</code>\n\n"
        "New row = new line\n\n"
        "<i>Each line becomes a new row of buttons.</i>",
        reply_markup=get_back_keyboard("menu_buttons")
    )
    await callback.answer()
