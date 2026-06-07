"""Channels Handler - Channel management."""
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from app.keyboards.admin_keyboards import get_channel_manager_keyboard, get_back_keyboard
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()


class ChannelStates(StatesGroup):
    waiting_channel_id = State()
    waiting_remove_id = State()


@router.callback_query(F.data == "menu_channels")
async def cb_channels_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    total = await db.channels.count_documents({})
    active = await db.channels.count_documents({"is_active": True})
    verified = await db.channels.count_documents({"is_verified": True})
    text = f"""
📢 <b>CHANNEL MANAGEMENT</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Channel Statistics:</b>
📢 Total Channels: <code>{total}</code>
✅ Active: <code>{active}</code>
🔐 Verified: <code>{verified}</code>
⏸️ Inactive: <code>{total - active}</code>
"""
    await callback.message.edit_text(text, reply_markup=get_channel_manager_keyboard())
    await callback.answer()


@router.callback_query(F.data == "ch_add")
async def cb_add_channel(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    await state.set_state(ChannelStates.waiting_channel_id)
    await callback.message.edit_text(
        "➕ <b>ADD CHANNEL</b>\n\n"
        "Forward any message from the channel\nOR send the Channel ID:\n\n"
        "<i>Example: -1001234567890</i>\n\n"
        "⚠️ Make sure the bot is admin in the channel!",
        reply_markup=get_back_keyboard("menu_channels")
    )
    await callback.answer()


@router.message(ChannelStates.waiting_channel_id)
async def process_add_channel(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    channel_id = None

    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        channel_name = message.forward_from_chat.title
        channel_username = message.forward_from_chat.username
    else:
        try:
            channel_id = int(message.text.strip())
            chat = await bot.get_chat(channel_id)
            channel_name = chat.title
            channel_username = chat.username
        except Exception:
            await message.answer("❌ Invalid channel ID or bot can't access the channel.")
            return

    db = get_db()
    existing = await db.channels.find_one({"channel_id": channel_id})
    if existing:
        await message.answer(f"⚠️ Channel <code>{channel_id}</code> already added!")
        return

    await db.channels.insert_one({
        "channel_id": channel_id,
        "channel_name": channel_name,
        "channel_username": channel_username,
        "is_active": True,
        "is_verified": False,
        "added_by": message.from_user.id,
        "added_at": __import__("datetime").datetime.utcnow(),
        "total_posts": 0,
        "member_count": 0,
    })
    await message.answer(
        f"✅ <b>Channel Added!</b>\n\n"
        f"📢 Name: <b>{channel_name}</b>\n"
        f"🆔 ID: <code>{channel_id}</code>\n"
        f"👤 Username: @{channel_username or 'N/A'}",
        reply_markup=get_channel_manager_keyboard()
    )


@router.callback_query(F.data == "ch_list")
async def cb_channel_list(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    channels = await db.channels.find({}).sort("added_at", -1).limit(15).to_list(15)
    text = "📋 <b>ALL CHANNELS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    if not channels:
        text += "<i>No channels added yet.</i>"
    else:
        for ch in channels:
            status = "✅" if ch.get("is_active") else "⏸️"
            verified = "🔐" if ch.get("is_verified") else "⚪"
            text += f"{status}{verified} <code>{ch['channel_id']}</code> | {ch.get('channel_name', 'N/A')[:25]}\n"
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_channels"))
    await callback.answer()
