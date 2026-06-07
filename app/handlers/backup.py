"""Backup Handler - Database backup and restore."""
import json
import logging
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, BufferedInputFile
from app.keyboards.admin_keyboards import get_backup_keyboard, get_back_keyboard
from app.utils.helpers import is_admin
from config.database import get_db

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "menu_backup")
async def cb_backup_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return
    text = """
💾 <b>BACKUP & RESTORE</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

🔒 <b>Data Protection System:</b>
💾 <b>Create Backup</b> - Export all data to JSON
🔄 <b>Restore</b> - Import from backup file
📋 <b>History</b> - View past backups
⏰ <b>Auto Backup</b> - Scheduled backups
📤 <b>Export DB</b> - Download database dump

⚠️ <b>Important:</b> Keep backups secure.
They contain all user and bot data.
"""
    await callback.message.edit_text(text, reply_markup=get_backup_keyboard())
    await callback.answer()


@router.callback_query(F.data == "backup_create")
async def cb_create_backup(callback: CallbackQuery, bot: Bot) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    await callback.answer("⏳ Creating backup...", show_alert=False)
    await callback.message.edit_text("⏳ <b>Creating backup...</b>\nThis may take a moment.")

    try:
        db = get_db()
        backup_data = {
            "created_at": datetime.utcnow().isoformat(),
            "created_by": callback.from_user.id,
            "version": "2.0.0",
            "collections": {}
        }

        collections = ["users", "posts", "channels", "advertisements",
                       "captions", "links", "button_templates", "bot_settings"]

        for coll_name in collections:
            docs = await db[coll_name].find({}).to_list(length=None)
            # Convert ObjectId and datetime to strings
            for doc in docs:
                doc.pop("_id", None)
                for k, v in doc.items():
                    if isinstance(v, datetime):
                        doc[k] = v.isoformat()
            backup_data["collections"][coll_name] = docs

        backup_json = json.dumps(backup_data, indent=2, default=str).encode("utf-8")
        filename = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        await bot.send_document(
            chat_id=callback.from_user.id,
            document=BufferedInputFile(backup_json, filename=filename),
            caption=(
                f"✅ <b>Backup Created Successfully!</b>\n\n"
                f"📅 Date: <code>{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</code>\n"
                f"📦 Size: <code>{len(backup_json) / 1024:.1f} KB</code>\n"
                f"🗂️ Collections: <code>{len(collections)}</code>"
            )
        )

        await callback.message.edit_text(
            "✅ <b>Backup sent to your DM!</b>",
            reply_markup=get_backup_keyboard()
        )
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        await callback.message.edit_text(
            f"❌ <b>Backup failed!</b>\n<code>{str(e)[:100]}</code>",
            reply_markup=get_back_keyboard("menu_backup")
        )
