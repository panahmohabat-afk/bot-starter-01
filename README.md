README.md
.gitignore
bot.py
pyTelegramBotAPI
pip install pyTelegramBotAPI
cd مسیر_پروژه
pip install pyTelegramBotAPI
import telebot
from telebot import types
from telethon import TelegramClient
from telethon.errors import UserNotParticipantError
import asyncio

# ======= تنظیمات ربات =======
TOKEN = "7739644433:AAGvaNWwMHiyaYzor9gI7Dqyp8JuX3BA_as"
bot = telebot.TeleBot(TOKEN)

CHANNEL_LINK = "https://t.me/+WmmdDIB3Pz9jZTE0"
GROUP_LINK   = "https://t.me/+bTD7ilyVMek0ZjI0"

# ======= Telethon برای چک عضویت =======
api_id = 1234567             # ← جایگزین کن با api_id خودت
api_hash = "API_HASH_تو"     # ← جایگزین کن با api_hash خودت
client = TelegramClient('session', api_id, api_hash)

# ======= فایل کاربران =======
USERS_FILE = "users.txt"
ADMIN_ID = 123456789         # ← شناسه مدیر

def add_user(user_id):
    with open(USERS_FILE, "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

# ======= متن خوش‌آمدگویی =======
WELCOME_TEXT = (
    "🌸 سلام دوست شاعر من! 🌸\n\n"
    "خوش آمدی به ربات پناه 🕊️\n\n"
    "برای فعال شدن ربات و استفاده از امکاناتش، ابتدا باید عضو کانال ما بشی:\n"
    f"🔗 کانال: {CHANNEL_LINK}\n\n"
    "بعد از عضویت، دکمه زیر رو بزن:\n"
    "✅ #عضو_کانال_شدم\n\n"
    "🎭 با ما در مسیر شعر و موسیقی همراه شو!"
)

# ======= منوی کاربران =======
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✅ #عضو_کانال_شدم")
    btn2 = types.KeyboardButton("⚙️ تنظیمات گروه")
    markup.add(btn1)
    markup.add(btn2)
    return markup

# ======= منوی مدیر =======
def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 آمار کاربران", "📝 ارسال پیام گروه")
    markup.add("⚙️ تنظیمات گروه")
    return markup

# ======= شروع ربات =======
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, WELCOME_TEXT)

# ======= مدیریت دکمه‌ها =======
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id

    # ==== چک عضویت کانال ====
    if message.text == "✅ #عضو_کانال_شدم":
        async def check_member():
            await client.start()
            try:
                participant = await client.get_participant(CHANNEL_LINK, user_id)
                if participant:
                    add_user(user_id)
                    bot.send_message(
                        message.chat.id,
                        f"🎉 عالی! تو عضو کانال هستی. حالا می‌تونی وارد گروه بشی:\n{GROUP_LINK}",
                        reply_markup=main_menu()
                    )
                else:
                    bot.send_message(message.chat.id, "❌ هنوز عضو کانال نشدی! لطفاً ابتدا عضو شو و دوباره بزن ✅")
            except UserNotParticipantError:
                bot.send_message(message.chat.id, "❌ هنوز عضو کانال نشدی! لطفاً ابتدا عضو شو و دوباره بزن ✅")
        asyncio.run(check_member())

    # ==== تنظیمات گروه ====
    elif message.text == "⚙️ تنظیمات گروه":
        if user_id == ADMIN_ID:
            bot.send_message(message.chat.id, "🔧 منوی مدیریتی باز شد:", reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "🔒 فقط مدیر می‌تواند وارد تنظیمات شود!")

    # ==== آمار کاربران ====
    elif message.text == "📊 آمار کاربران" and user_id == ADMIN_ID:
        with open(USERS_FILE, "r") as f:
            users = f.read().splitlines()
        bot.send_message(user_id, f"👥 تعداد کاربران ثبت شده: {len(users)}")

    # ==== ارسال پیام گروه ====
    elif message.text == "📝 ارسال پیام گروه" and user_id == ADMIN_ID:
        bot.send_message(user_id, "لطفا پیام خود را بفرستید. هر پیام بعدی برای همه کاربران ارسال می‌شود.")

        @bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
        def broadcast_message(m):
            with open(USERS_FILE, "r") as f:
                for uid in f.read().splitlines():
                    try:
                        bot.send_message(uid, f"📣 پیام مدیر:\n{m.text}")
                    except:
                        continue
            bot.send_message(ADMIN_ID, "✅ پیام با موفقیت ارسال شد!")

    # ==== پیام نامعتبر ====
    else:
        bot.send_message(message.chat.id, "لطفا از دکمه‌های منو استفاده کن ✅")

# ======= اجرای ربات =======
print("Bot is running...")
bot.infinity_polling()
