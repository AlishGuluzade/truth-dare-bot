# ‼️ Lazım olan kitabxanaları yükləyirik
import os
import json
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

from database import init_db, get_or_create_user, save_answer
# 🌱 .env faylından tokeni oxuyuruq
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# 📥 JSON faylından sualları oxuyan funksiya
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 🚀 /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    bot_user_id = get_or_create_user(telegram_id, username)

    await update.message.reply_text(
        f"🎲 Doğruluq və Cəsarət oyununa xoş gəldin!\n"
        f"Sənin istifadəçi ID-n: {bot_user_id}\n"
        f"Əmrlər: /truth /dare /play"
    )


# 🟢 /truth komandası
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_questions()
    question = random.choice(data["truth"])
    user_id = update.effective_user.id

    keyboard = [[
        InlineKeyboardButton("✅ Cavab verdim", callback_data=f"answered:{user_id}:truth")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🟢 Doğruluq sualı:\n{question}",
        reply_markup=reply_markup
    )

# 🔴 /dare komandası
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_questions()
    task = random.choice(data["dare"])
    user_id = update.effective_user.id

    keyboard = [[
        InlineKeyboardButton("✅ Cavab verdim", callback_data = f"answered:{user_id}:dare")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🔴 Cəsarət tapşırığı:\n{task}",
        reply_markup=reply_markup
    )

# ✅ Butona klik ediləndə işləyir
async def answered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_clicking = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    parts = query.data.split(":")
    expected_id = int(parts[1])
    question_type = parts[2] if len(parts) > 2 else "unknown"

    if user_clicking != expected_id:
        await query.answer("❗ Bu sual sənə aid deyil!", show_alert=True)
        return

    # DB-yə yaz
    bot_user_id = get_or_create_user(user_clicking, username)
    save_answer(bot_user_id, question_type)

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("🔁 Növbəti sual üçün: /truth /dare /play")

# 🔧 Bot tətbiqi qurulur
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("truth", truth))
app.add_handler(CommandHandler("dare", dare))
app.add_handler(CallbackQueryHandler(answered, pattern="^answered:"))

# 🧠 Bazanı hazırla və botu işə sal
init_db()
print("✅ Bot işə düşdü...")
app.run_polling()
