"""Media Library Handler."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.keyboards.admin_keyboards import get_back_keyboard
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()


@router.callback_query(F.data == "menu_media")
async def cb_media_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    db = get_db()
    total = await db.media_library.count_documents({})
    photos = await db.media_library.count_documents({"media_type": "photo"})
    videos = await db.media_library.count_documents({"media_type": "video"})
    docs = await db.media_library.count_documents({"media_type": "document"})

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📷 Photos", callback_data="media_photos"),
        InlineKeyboardButton(text="🎥 Videos", callback_data="media_videos"),
    )
    builder.row(
        InlineKeyboardButton(text="📄 Documents", callback_data="media_docs"),
        InlineKeyboardButton(text="🔍 Search Media", callback_data="media_search"),
    )
    builder.row(InlineKeyboardButton(text="◀️ Back", callback_data="admin_dashboard"))

    text = f"""
🖼️ <b>MEDIA LIBRARY</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

📊 <b>Media Statistics:</b>
🗂️ Total Files: <code>{total}</code>
📷 Photos: <code>{photos}</code>
🎥 Videos: <code>{videos}</code>
📄 Documents: <code>{docs}</code>

<i>Send any media to add it to your library!</i>
"""
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.message(F.photo | F.video | F.document | F.audio)
async def save_to_media_library(message: Message) -> None:
    if not is_admin(message.from_user.id):
        return
    db = get_db()
    from app.models.models import MediaLibraryModel, MediaType

    if message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        media_type = MediaType.PHOTO
    elif message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        media_type = MediaType.VIDEO
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        media_type = MediaType.DOCUMENT
    else:
        return

    existing = await db.media_library.find_one({"file_unique_id": file_unique_id})
    if not existing:
        media = MediaLibraryModel(
            file_id=file_id, file_unique_id=file_unique_id,
            media_type=media_type, uploaded_by=message.from_user.id,
            caption=message.caption,
        )
        await db.media_library.insert_one(media.dict())
        await message.reply("✅ Saved to media library!")
