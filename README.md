# نصب کتابخانه‌ها
# pip install python-telegram-bot==13.15

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# ===== تنظیمات ربات =====
TOKEN = "8244996074:AAGUWw2MH2QrX_GScgYWEcFk9Io1-BfVFKQ"

# لیست کانال‌ها برای عضویت اجباری
CHANNELS = ["@panah_channel_test", "@another_test_channel"]

USERS_FILE = "users.txt"
ADMIN_ID = 123456789  # ← شناسه ادمین

# ===== دکمه‌ها =====
keyboard = [
    ["🖤 شعر پناه", "📜 متن غمگین"],
    ["ℹ️ درباره ربات"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# دکمه شیشه‌ای نمونه
inline_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("کانال پناه 🌑", url="https://t.me/panah_channel_test")]
])


# ===== ذخیره کاربران =====
def add_user(user_id):
    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")


# ===== بررسی عضویت چند کانال =====
def check_membership(bot, user_id):
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


# ===== دستور /start =====
def start(update, context):
    user_id = update.effective_user.id

    if not check_membership(context.bot, user_id):
        text = "❌ برای استفاده از ربات، ابتدا عضو کانال‌ها شوید:\n"
        for ch in CHANNELS:
            text += f"https://t.me/{ch.replace('@','')}\n"
        text += "\nبعد /start بزنید."
        update.message.reply_text(text)
        return

    add_user(user_id)
    update.message.reply_text(
        "🌑 #پناه خوش آمدی!\nاز دکمه‌ها استفاده کن:",
        reply_markup=markup
    )
    update.message.reply_text("📌 کانال رسمی:", reply_markup=inline_buttons)


# ===== پیام‌ها =====
def handle_message(update, context):
    user_id = update.effective_user.id

    if not check_membership(context.bot, user_id):
        text = "❌ برای استفاده باید عضو کانال‌ها باشید:\n"
        for ch in CHANNELS:
            text += f"https://t.me/{ch.replace('@','')}\n"
        update.message.reply_text(text)
        return

    text = update.message.text

    if text == "🖤 شعر پناه":
        update.message.reply_text(
            "گاهی سکوت بلندتر از فریاد است...\n"
            "و پناه جایی‌ست که کسی صدایت را نمی‌شنود."
        )
    elif text == "📜 متن غمگین":
        update.message.reply_text(
            "بعضی آدم‌ها نمی‌روند...\nفقط کم‌رنگ می‌شوند در حافظه‌ات."
        )
    elif text == "ℹ️ درباره ربات":
        update.message.reply_text(
            "ربات شاعرانه پناه\nساخته شده برای متن‌های خاص و تاریک."
        )
    elif text == "📊 آمار کاربران" and user_id == ADMIN_ID:
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        update.message.reply_text(f"👥 تعداد کاربران ثبت شده: {len(users)}")
    elif text == "📣 ارسال پیام همگانی" and user_id == ADMIN_ID:
        update.message.reply_text("لطفاً پیام را ارسال کنید. هر پیام بعدی برای همه کاربران ارسال می‌شود.")
        context.user_data['broadcast'] = True
    elif context.user_data.get('broadcast') and user_id == ADMIN_ID:
        with open(USERS_FILE, "r") as f:
            for uid in f.read().splitlines():
                try:
                    context.bot.send_message(int(uid), f"📣 پیام مدیر:\n{text}")
                except:
                    continue
        update.message.reply_text("✅ پیام با موفقیت ارسال شد!")
        context.user_data['broadcast'] = False
    else:
        update.message.reply_text("⚠️ لطفا فقط از دکمه‌های منو استفاده کن!")


# ===== اجرا =====
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
