# نصب کتابخانه:
# pip install python-telegram-bot==13.15

from telegram.ext import Updater, CommandHandler

TOKEN = "7739644433:AAGvaNWwMHiyaYzor9gI7Dqyp8JuX3BA_as"

def start(update, context):
    update.message.reply_text("ربات وصل شد ✅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("Bot connected...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
