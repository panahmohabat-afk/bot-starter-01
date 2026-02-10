# نصب کتابخانه:
# pip install python-telegram-bot==13.15

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "8244996074:AAGUWw2MH2QrX_GScgYWEcFk9Io1-BfVFKQ"
CHANNEL = "@panah_channel_test"

def start(update, context):
    user_id = update.effective_user.id

    try:
        member = context.bot.get_chat_member(CHANNEL, user_id)

        if member.status not in ["member", "administrator", "creator"]:
            update.message.reply_text(
                "🔒 برای استفاده از ربات باید عضو کانال شوید:\n"
                f"https://t.me/{CHANNEL.replace('@','')}\n\n"
                "بعد از عضویت دوباره /start بزن."
            )
            return

    except:
        update.message.reply_text("خطا در بررسی عضویت کانال")
        return

    update.message.reply_text(
        "🎙️ به ربات دکلمه پناه خوش آمدی\n"
        "شعر و صدا اینجا شروع می‌شود..."
    )

def handle_message(update, context):
    update.message.reply_text("فقط /start بزن")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot connected...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
