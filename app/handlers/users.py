"""Users Handler - User management system."""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from app.keyboards.admin_keyboards import get_users_manager_keyboard, get_back_keyboard
from app.services.user_service import UserService
from app.services.security_service import SecurityService
from app.utils.helpers import is_admin

router = Router()


class UserStates(StatesGroup):
    waiting_ban_id = State()
    waiting_ban_reason = State()
    waiting_unban_id = State()
    waiting_promote_id = State()
    waiting_search = State()


@router.callback_query(F.data == "menu_users")
async def cb_users_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    svc = UserService()
    total = await svc.get_total_users()
    active = await svc.get_active_users()
    banned = await svc.get_banned_users_count()
    text = f"""
👥 <b>USER MANAGEMENT</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>User Statistics:</b>
👥 Total Users: <code>{total}</code>
🟢 Active (7d): <code>{active}</code>
🚫 Banned: <code>{banned}</code>
📈 New Today: <code>0</code>
"""
    await callback.message.edit_text(text, reply_markup=get_users_manager_keyboard())
    await callback.answer()


@router.callback_query(F.data == "user_ban")
async def cb_ban_user(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await state.set_state(UserStates.waiting_ban_id)
    await callback.message.edit_text(
        "🚫 <b>BAN USER</b>\n\nSend the User ID to ban:",
        reply_markup=get_back_keyboard("menu_users")
    )
    await callback.answer()


@router.message(UserStates.waiting_ban_id)
async def process_ban_id(message: Message, state: FSMContext) -> None:
    try:
        user_id = int(message.text.strip())
        await state.update_data(ban_user_id=user_id)
        await state.set_state(UserStates.waiting_ban_reason)
        await message.answer(f"Send ban reason for user <code>{user_id}</code>:")
    except ValueError:
        await message.answer("❌ Invalid User ID. Please send a number.")


@router.message(UserStates.waiting_ban_reason)
async def process_ban_reason(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_id = data["ban_user_id"]
    reason = message.text
    await state.clear()
    svc = UserService()
    success = await svc.ban_user(user_id=user_id, reason=reason, banned_by=message.from_user.id)
    sec = SecurityService()
    await sec.log_event(message.from_user.id, "ban", f"Banned user {user_id}: {reason}", severity="warning")
    if success:
        await message.answer(f"✅ User <code>{user_id}</code> has been banned.\n<b>Reason:</b> {reason}",
                             reply_markup=get_users_manager_keyboard())
    else:
        await message.answer(f"⚠️ User <code>{user_id}</code> not found or already banned.")


@router.callback_query(F.data == "user_unban")
async def cb_unban_user(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await state.set_state(UserStates.waiting_unban_id)
    await callback.message.edit_text(
        "✅ <b>UNBAN USER</b>\n\nSend the User ID to unban:",
        reply_markup=get_back_keyboard("menu_users")
    )
    await callback.answer()


@router.message(UserStates.waiting_unban_id)
async def process_unban_id(message: Message, state: FSMContext) -> None:
    try:
        user_id = int(message.text.strip())
        await state.clear()
        svc = UserService()
        success = await svc.unban_user(user_id)
        if success:
            await message.answer(f"✅ User <code>{user_id}</code> has been unbanned.",
                                 reply_markup=get_users_manager_keyboard())
        else:
            await message.answer(f"⚠️ User <code>{user_id}</code> not found.")
    except ValueError:
        await message.answer("❌ Invalid User ID.")
        await state.clear()


@router.message(Command("ban"))
async def cmd_ban(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("Usage: /ban <user_id> [reason]")
        return
    try:
        user_id = int(parts[1])
        reason = parts[2] if len(parts) > 2 else "No reason provided"
        svc = UserService()
        await svc.ban_user(user_id=user_id, reason=reason, banned_by=message.from_user.id)
        await message.answer(f"✅ Banned user <code>{user_id}</code>")
    except (ValueError, IndexError):
        await message.answer("❌ Invalid command format.")
