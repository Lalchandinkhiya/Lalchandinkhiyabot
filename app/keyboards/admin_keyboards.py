"""
Admin Keyboards Module
Premium inline keyboard layouts for the admin panel.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    """Main admin dashboard keyboard."""
    builder = InlineKeyboardBuilder()

    # Row 1: Core Management
    builder.row(
        InlineKeyboardButton(text="📝 Post Manager", callback_data="menu_posts"),
        InlineKeyboardButton(text="📢 Channels", callback_data="menu_channels"),
    )
    # Row 2: Tools
    builder.row(
        InlineKeyboardButton(text="✏️ Auto Caption", callback_data="menu_captions"),
        InlineKeyboardButton(text="🔗 Auto Links", callback_data="menu_links"),
    )
    # Row 3: More Tools
    builder.row(
        InlineKeyboardButton(text="🔘 Auto Buttons", callback_data="menu_buttons"),
        InlineKeyboardButton(text="📣 Advertisements", callback_data="menu_ads"),
    )
    # Row 4: Management
    builder.row(
        InlineKeyboardButton(text="👥 Users", callback_data="menu_users"),
        InlineKeyboardButton(text="🖼️ Media Library", callback_data="menu_media"),
    )
    # Row 5: System
    builder.row(
        InlineKeyboardButton(text="🛡️ Security", callback_data="menu_security"),
        InlineKeyboardButton(text="🔔 Notifications", callback_data="menu_notifications"),
    )
    # Row 6: System Tools
    builder.row(
        InlineKeyboardButton(text="💾 Backup", callback_data="menu_backup"),
        InlineKeyboardButton(text="📋 Logs", callback_data="menu_logs"),
    )
    # Row 7: Quick Actions
    builder.row(
        InlineKeyboardButton(text="📤 Broadcast", callback_data="broadcast_start"),
        InlineKeyboardButton(text="⚙️ Settings", callback_data="menu_settings"),
    )
    # Row 8: Refresh
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh Dashboard", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_post_manager_keyboard() -> InlineKeyboardMarkup:
    """Post management keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="➕ Create Post", callback_data="post_create"),
        InlineKeyboardButton(text="📋 All Posts", callback_data="post_list"),
    )
    builder.row(
        InlineKeyboardButton(text="✏️ Edit Post", callback_data="post_edit"),
        InlineKeyboardButton(text="🗑️ Delete Post", callback_data="post_delete"),
    )
    builder.row(
        InlineKeyboardButton(text="⏰ Schedule Post", callback_data="post_schedule"),
        InlineKeyboardButton(text="📑 Clone Post", callback_data="post_clone"),
    )
    builder.row(
        InlineKeyboardButton(text="👁️ Preview Post", callback_data="post_preview"),
        InlineKeyboardButton(text="📊 Analytics", callback_data="post_analytics"),
    )
    builder.row(
        InlineKeyboardButton(text="📡 Multi Channel Post", callback_data="post_multichannel"),
        InlineKeyboardButton(text="📁 Drafts", callback_data="post_drafts"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_caption_tools_keyboard() -> InlineKeyboardMarkup:
    """Auto caption tools keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="✨ Generate Caption", callback_data="caption_generate"),
        InlineKeyboardButton(text="📋 Templates", callback_data="caption_templates"),
    )
    builder.row(
        InlineKeyboardButton(text="🔧 Custom Template", callback_data="caption_custom"),
        InlineKeyboardButton(text="⚡ Dynamic Variables", callback_data="caption_variables"),
    )
    builder.row(
        InlineKeyboardButton(text="#️⃣ Hashtag Generator", callback_data="caption_hashtags"),
        InlineKeyboardButton(text="📌 Auto Footer", callback_data="caption_footer"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_link_tools_keyboard() -> InlineKeyboardMarkup:
    """Auto link tools keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🔄 Link Replacement", callback_data="link_replace"),
        InlineKeyboardButton(text="✂️ URL Shortener", callback_data="link_shorten"),
    )
    builder.row(
        InlineKeyboardButton(text="🤝 Referral Links", callback_data="link_referral"),
        InlineKeyboardButton(text="📊 Link Analytics", callback_data="link_analytics"),
    )
    builder.row(
        InlineKeyboardButton(text="🔍 Track Link", callback_data="link_track"),
        InlineKeyboardButton(text="📋 All Links", callback_data="link_list"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_button_tools_keyboard() -> InlineKeyboardMarkup:
    """Auto button tools keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="➕ Create Buttons", callback_data="btn_create"),
        InlineKeyboardButton(text="📋 Templates", callback_data="btn_templates"),
    )
    builder.row(
        InlineKeyboardButton(text="🔗 URL Buttons", callback_data="btn_url"),
        InlineKeyboardButton(text="⚙️ Callback Buttons", callback_data="btn_callback"),
    )
    builder.row(
        InlineKeyboardButton(text="📐 Multi Row", callback_data="btn_multirow"),
        InlineKeyboardButton(text="🤖 Auto Add Buttons", callback_data="btn_auto"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_ads_manager_keyboard() -> InlineKeyboardMarkup:
    """Advertisement manager keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🖼️ Banner Ads", callback_data="ad_banner"),
        InlineKeyboardButton(text="📝 Text Ads", callback_data="ad_text"),
    )
    builder.row(
        InlineKeyboardButton(text="➕ Create Ad", callback_data="ad_create"),
        InlineKeyboardButton(text="📋 All Ads", callback_data="ad_list"),
    )
    builder.row(
        InlineKeyboardButton(text="⏰ Scheduled Ads", callback_data="ad_scheduled"),
        InlineKeyboardButton(text="📊 Ad Analytics", callback_data="ad_analytics"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Rotation Settings", callback_data="ad_rotation"),
        InlineKeyboardButton(text="⚡ Priority Control", callback_data="ad_priority"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_security_keyboard() -> InlineKeyboardMarkup:
    """Security tools keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🔐 Admin Auth", callback_data="sec_auth"),
        InlineKeyboardButton(text="👮 Role Control", callback_data="sec_roles"),
    )
    builder.row(
        InlineKeyboardButton(text="🌐 IP Logging", callback_data="sec_ip_logs"),
        InlineKeyboardButton(text="🔑 Sessions", callback_data="sec_sessions"),
    )
    builder.row(
        InlineKeyboardButton(text="📋 Audit Logs", callback_data="sec_audit"),
        InlineKeyboardButton(text="🛡️ Anti Spam", callback_data="sec_antispam"),
    )
    builder.row(
        InlineKeyboardButton(text="🌊 Flood Protection", callback_data="sec_flood"),
        InlineKeyboardButton(text="✅ Channel Verify", callback_data="sec_channel_verify"),
    )
    builder.row(
        InlineKeyboardButton(text="🚫 Blacklist", callback_data="sec_blacklist"),
        InlineKeyboardButton(text="🎛️ Permissions", callback_data="sec_permissions"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_users_manager_keyboard() -> InlineKeyboardMarkup:
    """User management keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="👥 All Users", callback_data="user_list"),
        InlineKeyboardButton(text="🔍 Search User", callback_data="user_search"),
    )
    builder.row(
        InlineKeyboardButton(text="🚫 Ban User", callback_data="user_ban"),
        InlineKeyboardButton(text="✅ Unban User", callback_data="user_unban"),
    )
    builder.row(
        InlineKeyboardButton(text="👑 Promote Admin", callback_data="user_promote"),
        InlineKeyboardButton(text="⬇️ Demote Admin", callback_data="user_demote"),
    )
    builder.row(
        InlineKeyboardButton(text="📊 User Stats", callback_data="user_stats"),
        InlineKeyboardButton(text="📋 Export Users", callback_data="user_export"),
    )
    builder.row(
        InlineKeyboardButton(text="💬 Welcome Msg", callback_data="user_welcome"),
        InlineKeyboardButton(text="📌 Force Sub", callback_data="user_forcesub"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_backup_keyboard() -> InlineKeyboardMarkup:
    """Backup and restore keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="💾 Create Backup", callback_data="backup_create"),
        InlineKeyboardButton(text="📋 Backup History", callback_data="backup_list"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Restore Backup", callback_data="backup_restore"),
        InlineKeyboardButton(text="🗑️ Delete Backup", callback_data="backup_delete"),
    )
    builder.row(
        InlineKeyboardButton(text="⏰ Auto Backup", callback_data="backup_auto"),
        InlineKeyboardButton(text="📤 Export DB", callback_data="backup_export"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_logs_keyboard() -> InlineKeyboardMarkup:
    """Logs viewer keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📋 All Logs", callback_data="log_all"),
        InlineKeyboardButton(text="❌ Error Logs", callback_data="log_errors"),
    )
    builder.row(
        InlineKeyboardButton(text="🛡️ Security Logs", callback_data="log_security"),
        InlineKeyboardButton(text="👤 User Logs", callback_data="log_users"),
    )
    builder.row(
        InlineKeyboardButton(text="📤 Broadcast Logs", callback_data="log_broadcast"),
        InlineKeyboardButton(text="🗑️ Clear Logs", callback_data="log_clear"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()


def get_confirmation_keyboard(
    confirm_data: str,
    cancel_data: str = "admin_dashboard"
) -> InlineKeyboardMarkup:
    """Generic confirmation keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Confirm", callback_data=confirm_data),
        InlineKeyboardButton(text="❌ Cancel", callback_data=cancel_data),
    )
    return builder.as_markup()


def get_back_keyboard(back_data: str = "admin_dashboard") -> InlineKeyboardMarkup:
    """Simple back button keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data=back_data),
    )
    return builder.as_markup()


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu for regular users."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="ℹ️ About", callback_data="user_about"),
        InlineKeyboardButton(text="📞 Support", callback_data="user_support"),
    )
    return builder.as_markup()


def get_channel_manager_keyboard() -> InlineKeyboardMarkup:
    """Channel management keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="➕ Add Channel", callback_data="ch_add"),
        InlineKeyboardButton(text="📋 All Channels", callback_data="ch_list"),
    )
    builder.row(
        InlineKeyboardButton(text="✏️ Edit Channel", callback_data="ch_edit"),
        InlineKeyboardButton(text="🗑️ Remove Channel", callback_data="ch_remove"),
    )
    builder.row(
        InlineKeyboardButton(text="✅ Verify Channel", callback_data="ch_verify"),
        InlineKeyboardButton(text="📊 Channel Stats", callback_data="ch_stats"),
    )
    builder.row(
        InlineKeyboardButton(text="🤖 Bot Status", callback_data="ch_bot_status"),
        InlineKeyboardButton(text="📌 Set Footer", callback_data="ch_footer"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Menu", callback_data="admin_dashboard"),
    )

    return builder.as_markup()
