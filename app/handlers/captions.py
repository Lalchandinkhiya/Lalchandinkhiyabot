"""
Caption Tools Handler
Auto Caption Generator, Templates, Dynamic Variables, Hashtags, Footer.
"""

import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.keyboards.admin_keyboards import get_caption_tools_keyboard, get_back_keyboard
from app.utils.helpers import is_admin

router = Router()
logger = logging.getLogger(__name__)


class CaptionStates(StatesGroup):
    waiting_template_name = State()
    waiting_template_content = State()
    waiting_caption_topic = State()


@router.callback_query(F.data == "menu_captions")
async def cb_caption_menu(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
✏️ <b>AUTO CAPTION TOOLS</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

Automate your caption creation with:

✨ <b>AI Caption Generator</b> - AI-powered captions
📋 <b>Caption Templates</b> - Save & reuse templates
🔧 <b>Dynamic Variables</b> - Auto-fill with {date}, {time}, {channel}
#️⃣ <b>Hashtag Generator</b> - Topic-based hashtags
📌 <b>Auto Footer</b> - Always-appended footer text

<b>Available Variables:</b>
<code>{date}</code> → Current date
<code>{time}</code> → Current time
<code>{channel}</code> → Channel name
<code>{post_count}</code> → Post number
<code>{admin_name}</code> → Posting admin
"""
    await callback.message.edit_text(text, reply_markup=get_caption_tools_keyboard())
    await callback.answer()


@router.callback_query(F.data == "caption_generate")
async def cb_generate_caption(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    await state.set_state(CaptionStates.waiting_caption_topic)
    await callback.message.edit_text(
        "✨ <b>AI CAPTION GENERATOR</b>\n\n"
        "Send me the topic/keywords for your caption:\n\n"
        "<i>Example: 'new product launch smartphone'</i>",
        reply_markup=get_back_keyboard("menu_captions")
    )
    await callback.answer()


@router.message(CaptionStates.waiting_caption_topic)
async def process_caption_topic(message: Message, state: FSMContext) -> None:
    topic = message.text
    await state.clear()

    # Generate captions based on topic
    now = __import__("datetime").datetime.utcnow()
    caption = (
        f"🔥 <b>{topic.title()}</b>\n\n"
        f"📅 {now.strftime('%B %d, %Y')}\n"
        f"⏰ {now.strftime('%I:%M %p')} UTC\n\n"
        f"💡 Stay tuned for more updates!\n"
        f"#{'#'.join(topic.split()[:3])}"
    )

    await message.answer(
        f"✅ <b>Generated Caption:</b>\n\n"
        f"<code>{caption}</code>\n\n"
        f"<i>Copy and use in your posts!</i>",
        reply_markup=get_back_keyboard("menu_captions")
    )


@router.callback_query(F.data == "caption_hashtags")
async def cb_hashtag_gen(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
#️⃣ <b>HASHTAG GENERATOR</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

<b>Popular Hashtag Categories:</b>

📱 Tech: <code>#tech #technology #innovation #digital</code>
📰 News: <code>#news #breaking #update #today</code>
💼 Business: <code>#business #startup #entrepreneur</code>
🎯 Marketing: <code>#marketing #promotion #viral</code>
📸 Media: <code>#photo #video #content #media</code>

<i>Send a topic to auto-generate relevant hashtags!</i>
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_captions"))
    await callback.answer()


@router.callback_query(F.data == "caption_footer")
async def cb_auto_footer(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access Denied!", show_alert=True)
        return

    text = """
📌 <b>AUTO FOOTER ADDER</b>
<code>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</code>

Auto-append footer to all posts.

<b>Current Footer:</b>
<i>Not configured</i>

<b>Example footer:</b>
<code>━━━━━━━━━━━━━━━━━━━
📢 @YourChannel | Follow for more!
🔔 Enable notifications to stay updated</code>

Use /setfooter [text] to configure.
"""
    await callback.message.edit_text(text, reply_markup=get_back_keyboard("menu_captions"))
    await callback.answer()
