import os
import sqlite3

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
INSTAGRAM_LINK = os.environ.get(
    "INSTAGRAM_LINK",
    "https://www.diskwala.com/app/6ac245893727384d45eabd00"
)

DB = "bot.db"


def database():
    con = sqlite3.connect(DB)

    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            balance REAL DEFAULT 0,
            status TEXT DEFAULT 'Active'
        )
    """)

    con.commit()
    return con


def main_menu():
    keyboard = [
        ["💎 Get Information"],
        ["📥 Instagram Download"],
        ["💰 My Balance", "📊 My Status"],
        ["🌐 Global Information", "📧 Temp Mail"],
        ["👤 My Profile", "🛟 Support"],
        ["ℹ️ About Bot"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    con = database()

    con.execute(
        "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
        (user.id, user.full_name)
    )

    con.execute(
        "UPDATE users SET name=? WHERE user_id=?",
        (user.full_name, user.id)
    )

    con.commit()
    con.close()

    text = f"""
👑 WELCOME TO INFORMATION BOT ✅

👤 Hello {user.first_name}!

🔐 यहाँ आपको सामान्य information
और useful services मिलेंगी।

━━━━━━━━━━━━━━━━━━━━

👇 नीचे से कोई option चुनें:
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    message = update.message.text

    con = database()

    row = con.execute(
        "SELECT balance, status FROM users WHERE user_id=?",
        (
