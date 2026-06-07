# 🔱 LALCHAND INKHIYA BOT

<div align="center">

```
██╗      █████╗ ██╗      ██████╗██╗  ██╗ █████╗ ███╗   ██╗
██║     ██╔══██╗██║     ██╔════╝██║  ██║██╔══██╗████╗  ██║
██║     ███████║██║     ██║     ███████║███████║██╔██╗ ██║
██║     ██╔══██║██║     ██║     ██╔══██║██╔══██║██║╚██╗██║
███████╗██║  ██║███████╗╚██████╗██║  ██║██║  ██║██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

██╗███╗   ██╗██╗  ██╗██╗  ██╗██╗██╗   ██╗ █████╗
██║████╗  ██║██║ ██╔╝██║  ██║██║╚██╗ ██╔╝██╔══██╗
██║██╔██╗ ██║█████╔╝ ███████║██║ ╚████╔╝ ███████║
██║██║╚██╗██║██╔═██╗ ██╔══██║██║  ╚██╔╝  ██╔══██║
██║██║ ╚████║██║  ██╗██║  ██║██║   ██║   ██║  ██║
╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝
```

**Premium Telegram Bot | Production-Ready | Aiogram 3.x | MongoDB**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram)](https://aiogram.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb)](https://mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
- [📖 Usage Guide](#-usage-guide)
- [🛡️ Security Features](#️-security-features)
- [🗃️ Database Schema](#️-database-schema)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

### 🎛️ Admin Dashboard
- 📊 Real-time statistics (users, posts, channels, broadcasts)
- ⏱️ Bot uptime display
- 🗃️ Database health monitoring
- 🔧 Maintenance mode toggle
- 👑 Multi-admin support

### 📝 Post Management (9 Tools)
| Feature | Description |
|---------|-------------|
| ➕ Create Post | Text, photo, video, document posts |
| ✏️ Edit Post | Modify existing posts |
| 🗑️ Delete Post | Soft-delete with status tracking |
| ⏰ Schedule Post | Publish at a specific date/time |
| 📑 Clone Post | Duplicate any existing post |
| 👁️ Preview Post | Preview before publishing |
| 📡 Multi-Channel | Post to multiple channels at once |
| 📁 Drafts | Save and manage post drafts |
| 📊 Analytics | Views, forwards, reactions tracking |

### ✏️ Auto Caption Tools (5 Tools)
- ✨ AI Caption Generator
- 📋 Custom Caption Templates
- ⚡ Dynamic Variables (`{date}`, `{time}`, `{channel}`, etc.)
- #️⃣ Hashtag Generator
- 📌 Auto Footer Adder

### 🔗 Auto Link Tools (5 Tools)
- 🔄 Auto Link Replacement
- ✂️ URL Shortener (Bitly/TinyURL)
- 🤝 Auto Referral Link Inserter
- 🔍 Link Tracking
- 📊 Link Analytics (clicks, unique visitors)

### 🔘 Auto Button Tools (6 Tools)
- ➕ Inline Button Creator
- 🤖 Auto Button Adder to Posts
- 🔗 URL Buttons
- ⚙️ Callback Buttons
- 📐 Multi-Row Button Layouts
- 📋 Button Templates

### 📣 Advertisement Management (6 Features)
- 🖼️ Banner Ads Manager
- 📝 Text Ads Manager
- ⏰ Scheduled Advertisements
- 📊 Advertisement Analytics
- 🔄 Priority-based Rotation System
- ⚡ Ad Priority Control (1-10)

### 🛡️ Security Tools (10 Advanced Features)
1. 🔐 Admin Authentication
2. 👮 Role-Based Access Control (User/Moderator/Admin/SuperAdmin)
3. 🌐 IP Address Logging
4. 🔑 Session Management (auto-expire)
5. 📋 Login Audit Logs
6. 🛡️ Anti-Spam Protection
7. 🌊 Flood Protection (rate limiting)
8. ✅ Channel Verification
9. 🚫 User Blacklist System
10. 🎛️ Command Permission Control

### 🌟 Additional Features
- 💬 Welcome Messages
- 📌 Force Subscribe System
- 👥 User Management (ban/unban/promote)
- 📢 Channel Management
- 🖼️ Media Library
- 💾 Backup & Restore System
- 🔔 Notification Center
- 📋 Logs Viewer
- ❌ Error Monitoring
- 🔧 Maintenance Mode
- 👑 Multi-Admin Support
- 📤 Mass Broadcast with Statistics

---

## 📁 Project Structure

```
lalchand_inkhiya_bot/
│
├── main.py                          # 🚀 Bot entry point
├── requirements.txt                 # 📦 Python dependencies
├── .env.example                     # ⚙️ Environment variables template
├── .gitignore                       # 🙈 Git ignore rules
├── railway.toml                     # 🚂 Railway deployment config
├── render.yaml                      # 🎨 Render deployment config
│
├── config/                          # ⚙️ Configuration modules
│   ├── __init__.py
│   ├── settings.py                  # App settings (Pydantic)
│   └── database.py                  # MongoDB connection & indexes
│
├── app/                             # 🤖 Main application
│   ├── __init__.py
│   │
│   ├── handlers/                    # 📨 Message & callback handlers
│   │   ├── __init__.py
│   │   ├── start.py                 # /start, dashboard
│   │   ├── admin.py                 # Broadcast, maintenance, settings
│   │   ├── posts.py                 # Post management
│   │   ├── captions.py              # Caption tools
│   │   ├── links.py                 # Link tools
│   │   ├── buttons.py               # Button tools
│   │   ├── advertisements.py        # Ad management
│   │   ├── security.py              # Security features
│   │   ├── users.py                 # User management
│   │   ├── channels.py              # Channel management
│   │   ├── media.py                 # Media library
│   │   ├── backup.py                # Backup & restore
│   │   ├── notifications.py         # Notification center
│   │   └── logs.py                  # Log viewer
│   │
│   ├── middlewares/                 # 🔒 Aiogram middlewares
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication & ban checks
│   │   ├── anti_spam.py             # Flood & spam protection
│   │   ├── logging_middleware.py    # Request logging
│   │   └── maintenance.py           # Maintenance mode gate
│   │
│   ├── keyboards/                   # ⌨️ Inline keyboards
│   │   ├── __init__.py
│   │   └── admin_keyboards.py       # All admin panel keyboards
│   │
│   ├── models/                      # 📐 Pydantic data models
│   │   ├── __init__.py
│   │   └── models.py                # All DB collection models
│   │
│   ├── services/                    # 🔧 Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py          # User CRUD operations
│   │   ├── post_service.py          # Post CRUD operations
│   │   ├── stats_service.py         # Statistics aggregation
│   │   ├── security_service.py      # Security & audit logging
│   │   ├── notification_service.py  # Push notifications
│   │   └── scheduler.py             # Background tasks
│   │
│   └── utils/                       # 🛠️ Utility functions
│       ├── __init__.py
│       ├── helpers.py               # Common helper functions
│       ├── logger.py                # Logging configuration
│       ├── startup_banner.py        # ASCII art banner
│       └── bot_commands.py          # Bot command registration
│
├── docker/                          # 🐳 Docker configuration
│   ├── Dockerfile                   # Bot container image
│   └── docker-compose.yml           # Full stack (bot + MongoDB)
│
├── .github/
│   └── workflows/
│       └── deploy.yml               # CI/CD pipeline
│
├── logs/                            # 📋 Log files (auto-created)
└── backups/                         # 💾 Backup files (auto-created)
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.11+
- MongoDB 6.0+ (local or Atlas)
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/lalchand-inkhiya-bot.git
cd lalchand-inkhiya-bot
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate          # Linux/Mac
# OR
venv\Scripts\activate             # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
nano .env     # Edit with your values
```

### Step 5: Run the Bot
```bash
python main.py
```

---

## 🔧 Configuration

Edit `.env` file with your credentials:

```env
# Required
BOT_TOKEN=your_bot_token_here
SUPER_ADMIN_ID=your_telegram_id
MONGODB_URI=mongodb://localhost:27017
SECRET_KEY=your_random_32_char_secret

# Optional
ADMIN_IDS=id1,id2,id3
FLOOD_RATE=30
LOG_LEVEL=INFO
```

**Get your Telegram ID:** Message [@userinfobot](https://t.me/userinfobot)

**Get Bot Token:** Message [@BotFather](https://t.me/BotFather) → `/newbot`

---

## 🚀 Deployment

### 🐳 Docker (Recommended)

```bash
# Build and start all services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### 🖥️ VPS Deployment (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update && sudo apt install -y python3.11 python3.11-venv mongodb

# Start MongoDB
sudo systemctl enable mongod && sudo systemctl start mongod

# Setup bot
git clone https://github.com/yourusername/lalchand-inkhiya-bot.git
cd lalchand-inkhiya-bot
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env

# Run with systemd (auto-restart)
sudo nano /etc/systemd/system/lalchand-bot.service
```

**Systemd service file:**
```ini
[Unit]
Description=Lalchand Inkhiya Telegram Bot
After=network.target mongod.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/lalchand-inkhiya-bot
ExecStart=/home/ubuntu/lalchand-inkhiya-bot/venv/bin/python main.py
Restart=always
RestartSec=10
EnvironmentFile=/home/ubuntu/lalchand-inkhiya-bot/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable lalchand-bot
sudo systemctl start lalchand-bot
sudo journalctl -u lalchand-bot -f   # View logs
```

### 🚂 Railway Deployment

1. Fork this repository
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables from `.env.example`
5. Add a MongoDB plugin (Railway provides free MongoDB)
6. Deploy!

### 🎨 Render Deployment

1. Fork this repository
2. Go to [render.com](https://render.com) → New → Worker
3. Connect your GitHub repository
4. Add environment variables
5. Deploy!

---

## 📖 Usage Guide

### Admin Commands
| Command | Description |
|---------|-------------|
| `/start` | Open admin dashboard |
| `/stats` | Quick statistics |
| `/broadcast` | Send broadcast to all users |
| `/ban <user_id> [reason]` | Ban a user |
| `/unban <user_id>` | Unban a user |
| `/addadmin <user_id>` | Add new admin (Super Admin only) |
| `/maintenance` | Toggle maintenance mode |
| `/backup` | Create database backup |
| `/logs` | View recent logs |

### Creating a Post
1. Go to 📝 **Post Manager**
2. Click ➕ **Create Post**
3. Enter title → content → media (optional)
4. Post is saved as draft
5. Choose: Publish now / Schedule / Edit

### Broadcasting a Message
1. From dashboard, click 📤 **Broadcast**
2. Send your message (text, photo, or video)
3. Bot will broadcast to all active users
4. View real-time progress and final stats

### Adding a Channel
1. Go to 📢 **Channels**
2. Click ➕ **Add Channel**
3. Forward any message from the channel, OR send the channel ID
4. Ensure bot is admin in the channel first!

---

## 🛡️ Security Features

### Role Hierarchy
```
👑 Super Admin  →  Full control, can add/remove admins
🔴 Admin        →  Manage posts, users, broadcasts
🟡 Moderator    →  View & moderate content
🟢 User         →  Standard bot access
```

### Flood Protection
- Max 30 messages/minute per user (configurable)
- 3 warnings before mute
- 60-second automatic mute on flood detection
- All events logged to security audit trail

---

## 🗃️ Database Schema

### Collections
| Collection | Purpose |
|------------|---------|
| `users` | User profiles, roles, activity |
| `posts` | Post content, status, analytics |
| `channels` | Managed channels |
| `broadcasts` | Broadcast history & stats |
| `advertisements` | Ad campaigns |
| `captions` | Caption templates |
| `links` | Link tracking data |
| `button_templates` | Saved button layouts |
| `security_logs` | Audit trail (TTL: 90 days) |
| `sessions` | Admin sessions (TTL: auto-expire) |
| `blacklist` | Banned users |
| `media_library` | Uploaded media files |
| `bot_settings` | Bot configuration |
| `notifications` | User notifications (TTL: 30 days) |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ | Aiogram 3.x | MongoDB | Python 3.11**

⭐ Star this repo if you found it useful!

</div>
