# ======================================================
# Bot حرفه‌ای چک عضویت کانال | بدون دکمه، آماده اجرا
# ======================================================

# ===== نصب کتابخانه‌ها =====
# قبل از اجرا در ترمینال:
# pip install python-telegram-bot --upgrade

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ===== توکن ربات و کانال =====
TOKEN = '7739644433:AAGvaNWwMHiyaYzor9gI7Dqyp8JuX3BA_as'
CHANNEL = '@YourChannelName'  # ← نام کانال واقعی با @ یا لینک کامل

# ===== فایل ذخیره کاربران =====
USERS_FILE = "users.txt"

def add_user(user_id):
    """افزودن کاربر به فایل"""
    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

# ===== دستور /start =====
def start(update, context):
    user_id = update.effective_user.id           # شناسه کاربر
    member = context.bot.get_chat_member(CHANNEL, user_id)  # بررسی عضویت کانال

    if member.status not in ['member', 'administrator', 'creator']:
        # اگر عضو نیست پیام بده
        update.message.reply_text(
            f'❌ برای استفاده از ربات باید عضو کانال {CHANNEL} باشید!\nلطفاً عضو شوید و دوباره امتحان کنید.'
        )
    else:
        add_user(user_id)  # ذخیره کاربر در فایل
        update.message.reply_text(
            '🎉 به ربات خوش آمدید! شما عضو کانال هستید.'
        )

# ===== پیام نامعتبر =====
def handle_message(update, context):
    update.message.reply_text(
        "⚠️ لطفا فقط از دستور /start استفاده کنید و عضو کانال باشید!"
    )

# ===== اجرای ربات =====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # دستور /start
    dp.add_handler(CommandHandler('start', start))

    # سایر پیام‌ها
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # شروع ربات
    print("Bot is running...")
    updater.start_polling()
    updater.idle()  # ← ربات همیشه آنلاین بماند

# ===== شروع برنامه =====
if __name__ == "__main__":
    main()
