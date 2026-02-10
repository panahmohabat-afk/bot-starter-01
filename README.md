# ======================================================
# Bot حرفه‌ای چک عضویت کانال | بدون دکمه، آماده اجرا
# ======================================================

# ======= نصب کتابخانه‌ها =======
# قبل از اجرای ربات در ترمینال این دستور را اجرا کنید:
# pip install python-telegram-bot --upgrade

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ===== توکن ربات و کانال =====
TOKEN = '7739644433:AAGvaNWwMHiyaYzor9gI7Dqyp8JuX3BA_as'
CHANNEL = '@YourChannelName'  # ← نام کانال خودت را اینجا بزار

# ===== دستور start =====
def start(update, context):
    user_id = update.effective_user.id
    member = context.bot.get_chat_member(CHANNEL, user_id)
    
    if member.status not in ['member', 'administrator', 'creator']:
        # اگر عضو نیست پیام بده
        update.message.reply_text(
            f'برای استفاده از ربات باید عضو کانال {CHANNEL} باشید!\nلطفاً عضو شوید و دوباره امتحان کنید.'
        )
    else:
        update.message.reply_text('به ربات خوش آمدید! شما عضو کانال هستید.')

# ===== اجرای ربات =====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

# ===== شروع برنامه =====
if __name__ == "__main__":
    main()
