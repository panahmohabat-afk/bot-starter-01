# ===== نصب =====
# pip install python-telegram-bot==13.15

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ===== توکن =====
TOKEN = "8244996074:AAGUWw2MH2QrX_GScgYWEcFk9Io1-BfVFKQ"

# ===== دستور start =====
def start(update, context):
    update.message.reply_text("ربات وصل شد ✅")

# ===== پیام‌های دیگر =====
def handle_message(update, context):
    update.message.reply_text("فقط /start بزن")

# ===== اجرای ربات =====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
