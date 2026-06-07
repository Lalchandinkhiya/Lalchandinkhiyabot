"""
Posts Handler Module
Full post management: create, edit, delete, schedule, clone, preview, analytics.
"""

import logging
from datetime import datetime
from typing import Optional

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.keyboards.admin_keyboards import (
    get_post_manager_keyboard,
    get_back_keyboard,
    get_confirmation_keyboard,
)
from app.services.post_service import PostService
from app.utils.helpers import is_admin

router = Router()
logger = logging.getLogger(__name__)


class PostStates(StatesGroup):
    waiting_title = State()
    waiting_content = State()
    waiting_media = State()
    waiting_caption = State()
    waiting_schedule_time = State()
    waiting_edit_post_id = State()
    waiting_edit_content = State()
    waiting_delete_post_id = State()
    waiting_clone_post_id = State()
    selecting_channels = State()


# ── Post Manager Menu ──────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_posts")
async def cb_post_manager(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    svc = PostService()
    total = await svc.get_total_posts()
    drafts = await svc.get_drafts_count()
    scheduled = await svc.get_scheduled_count()

    text = f"""
📝 <b>POST MANAGER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Post Statistics:</b>
📝 Total Posts: <code>{total}</code>
📁 Drafts: <code>{drafts}</code>
⏰ Scheduled: <code>{scheduled}</code>
✅ Published: <code>{total - drafts - scheduled}</code>

<b>Select an action:</b>
"""
    await callback.message.edit_text(text, reply_markup=get_post_manager_keyboard())
    await callback.answer()


# ── Create Post ────────────────────────────────────────────────────────────

@router.callback_query(F.data == "post_create")
async def cb_create_post(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    await state.set_state(PostStates.waiting_title)
    text = """
➕ <b>CREATE NEW POST</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Step 1/4: Post Title</b>
Please send me the title for this post.

<i>Example: "Breaking News Update"</i>

/cancel - Cancel creation
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_posts"))
    await callback.answer()


@router.message(PostStates.waiting_title)
async def process_post_title(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await state.clear()
        await message.answer("❌ Post creation cancelled.", reply_markup=get_post_manager_keyboard())
        return

    await state.update_data(title=message.text)
    await state.set_state(PostStates.waiting_content)

    await message.answer(
        "✅ Title saved!\n\n"
        "<b>Step 2/4: Post Content</b>\n"
        "Send the text content for your post.\n\n"
        "<i>You can use HTML formatting: &lt;b&gt;bold&lt;/b&gt;, &lt;i&gt;italic&lt;/i&gt;</i>\n\n"
        "/skip - Skip content (media-only post)\n"
        "/cancel - Cancel"
    )


@router.message(PostStates.waiting_content)
async def process_post_content(message: Message, state: FSMContext) -> None:
    content = None if message.text == "/skip" else message.text

    if message.text == "/cancel":
        await state.clear()
        await message.answer("❌ Cancelled.", reply_markup=get_post_manager_keyboard())
        return

    await state.update_data(content=content)
    await state.set_state(PostStates.waiting_media)

    await message.answer(
        "✅ Content saved!\n\n"
        "<b>Step 3/4: Media (Optional)</b>\n"
        "Send a photo, video, or document to attach.\n\n"
        "/skip - Skip (text-only post)\n"
        "/cancel - Cancel"
    )


@router.message(PostStates.waiting_media, F.photo | F.video | F.document | F.audio)
async def process_post_media(message: Message, state: FSMContext) -> None:
    media_file_id = None
    media_type = None

    if message.photo:
        media_file_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_file_id = message.video.file_id
        media_type = "video"
    elif message.document:
        media_file_id = message.document.file_id
        media_type = "document"
    elif message.audio:
        media_file_id = message.audio.file_id
        media_type = "audio"

    await state.update_data(media_file_id=media_file_id, media_type=media_type)
    await _finalize_post_creation(message, state)


@router.message(PostStates.waiting_media, F.text == "/skip")
async def skip_post_media(message: Message, state: FSMContext) -> None:
    await state.update_data(media_file_id=None, media_type=None)
    await _finalize_post_creation(message, state)


async def _finalize_post_creation(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    svc = PostService()
    post = await svc.create_post(
        title=data["title"],
        content=data.get("content"),
        media_file_id=data.get("media_file_id"),
        media_type=data.get("media_type"),
        created_by=message.from_user.id,
    )

    await message.answer(
        f"✅ <b>Post Created Successfully!</b>\n\n"
        f"🆔 Post ID: <code>{post['post_id']}</code>\n"
        f"📝 Title: <b>{post['title']}</b>\n"
        f"📊 Status: <code>Draft</code>\n\n"
        f"<i>Your post has been saved as a draft.</i>",
        reply_markup=get_post_manager_keyboard()
    )


# ── List Posts ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "post_list")
async def cb_post_list(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    svc = PostService()
    posts = await svc.get_recent_posts(limit=10)

    text = "📋 <b>ALL POSTS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"

    if not posts:
        text += "<i>No posts found. Create your first post!</i>"
    else:
        for post in posts:
            status_icons = {
                "draft": "📁", "scheduled": "⏰",
                "published": "✅", "deleted": "🗑️", "failed": "❌"
            }
            icon = status_icons.get(post.get("status", "draft"), "📝")
            created = post.get("created_at", datetime.utcnow()).strftime("%m/%d")
            text += (
                f"{icon} <code>{post['post_id']}</code> | "
                f"<b>{post.get('title', 'Untitled')[:25]}</b> | {created}\n"
            )

    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_posts"))
    await callback.answer()


# ── Schedule Post ──────────────────────────────────────────────────────────

@router.callback_query(F.data == "post_schedule")
async def cb_schedule_post(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    await state.set_state(PostStates.waiting_edit_post_id)
    await state.update_data(action="schedule")
    await callback.message.edit_text(
        "⏰ <b>SCHEDULE POST</b>\n\n"
        "Enter the Post ID to schedule:\n"
        "<i>Find IDs in the post list</i>",
        reply_markup=get_back_keyboard("menu_posts")
    )
    await callback.answer()


# ── Post Drafts ────────────────────────────────────────────────────────────

@router.callback_query(F.data == "post_drafts")
async def cb_post_drafts(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    svc = PostService()
    drafts = await svc.get_drafts(limit=10)

    text = "📁 <b>SAVED DRAFTS</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"

    if not drafts:
        text += "<i>No drafts found.</i>"
    else:
        for draft in drafts:
            created = draft.get("created_at", datetime.utcnow()).strftime("%m/%d %H:%M")
            text += f"📁 <code>{draft['post_id']}</code> | <b>{draft.get('title', 'Untitled')[:30]}</b> | {created}\n"

    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_posts"))
    await callback.answer()


# ── Post Analytics ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "post_analytics")
async def cb_post_analytics(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    svc = PostService()
    stats = await svc.get_overall_analytics()

    text = f"""
📊 <b>POST ANALYTICS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📈 <b>Overall Performance:</b>
📝 Total Posts: <code>{stats['total']}</code>
✅ Published: <code>{stats['published']}</code>
📁 Drafts: <code>{stats['drafts']}</code>
⏰ Scheduled: <code>{stats['scheduled']}</code>

👁️ <b>Engagement:</b>
👁️ Total Views: <code>{stats['total_views']}</code>
↗️ Total Forwards: <code>{stats['total_forwards']}</code>
❤️ Total Reactions: <code>{stats['total_reactions']}</code>

📅 <b>This Week:</b>
📝 Posts Created: <code>{stats['this_week']}</code>
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_posts"))
    await callback.answer()


# ── Multi Channel Post ─────────────────────────────────────────────────────

@router.callback_query(F.data == "post_multichannel")
async def cb_multichannel_post(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    from config.database import get_db
    db = get_db()
    channels = await db.channels.find({"is_active": True}).to_list(length=20)

    text = "📡 <b>MULTI CHANNEL POSTING</b>\n<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
    text += f"<b>Active Channels ({len(channels)}):</b>\n\n"

    for ch in channels:
        text += f"📢 <code>{ch['channel_id']}</code> - {ch.get('channel_name', 'Unknown')}\n"

    if not channels:
        text += "<i>No channels added yet. Add channels first!</i>"

    text += "\n\n<i>To post to multiple channels, create a post and select target channels.</i>"

    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_posts"))
    await callback.answer()
