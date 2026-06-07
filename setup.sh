#!/bin/bash
# ═══════════════════════════════════════════════════
#   LALCHAND INKHIYA BOT — Quick Setup Script
# ═══════════════════════════════════════════════════

echo "🔱 Setting up Lalchand Inkhiya Bot..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Setup .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  .env file created! Please fill in your values:"
    echo "   nano .env"
    echo ""
    echo "   Required fields:"
    echo "   ✏️  BOT_TOKEN      → from @BotFather"
    echo "   ✏️  SUPER_ADMIN_ID → your Telegram ID"
    echo "   ✏️  MONGODB_URI    → your MongoDB URL"
    echo "   ✏️  SECRET_KEY     → any random string"
else
    echo "✅ .env already exists"
fi

# Create directories
mkdir -p logs backups

echo ""
echo "✅ Setup complete!"
echo "📌 Run: source venv/bin/activate && python main.py"
