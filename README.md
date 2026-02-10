# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "TOKEN_HERE"   # ← 8244996074:AAGUWw2MH2QrX_GScgYWEcFk9Io1-BfVFKQ
CHANNELS = ["@YourChannel"]  # ← آیدی کانالت

users = set()

# چک عضویت
def check_membership(bot, user_id):
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# استارت
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not check_membership(context.bot, user_id):
        text = "❌ اول عضو کانال شو:\n"
        buttons = []
        for ch in CHANNELS:
            link = f"https://t.me/{ch.replace('@','')}"
            text += link + "\n"
            buttons.append([InlineKeyboardButton("عضویت", url=link)])

        update.message.reply_text(
            text + "\nبعدش /start بزن",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    users.add(user_id)

    keyboard = [
        ["📢 کانال"],
        ["👤 پنل من"]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        "🔥 ربات پناه فعال شد\nاز دکمه‌ها استفاده کن",
        reply_markup=markup
    )

# پیام‌ها
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "📢 کانال":
        update.message.reply_text("https://t.me/YourChannel")

    elif text == "👤 پنل من":
        update.message.reply_text(f"آیدی: {update.effective_user.id}")

    else:
        update.message.reply_text("دستور نامعتبر")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot running...")
    updater.start_polling()
    updater.idle()

if name == "main":
    main()
