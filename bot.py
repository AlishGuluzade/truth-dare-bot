# ‼️ the necessary libraries
import os
import json
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

from database import init_db, get_or_create_user, save_answer
# 🌱 .env Read TOCKEN
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# 📥 JSON Read Questions
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    bot_user_id = get_or_create_user(telegram_id, username)

    await update.message.reply_text(
        f"🎲 Welcome to Truth and Dare Game!\n"
        f"Your ID is: {bot_user_id}\n"
        f"Commands: /truth /dare "
    )


# 🟢 /truth command
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_questions()
    question = random.choice(data["truth"])
    user_id = update.effective_user.id

    keyboard = [[
        InlineKeyboardButton("✅ Answered", callback_data=f"answered:{user_id}:truth")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🟢 Truth question:\n{question}",
        reply_markup=reply_markup
    )

# 🔴 /dare command
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_questions()
    task = random.choice(data["dare"])
    user_id = update.effective_user.id

    keyboard = [[
        InlineKeyboardButton("✅ Answered", callback_data = f"answered:{user_id}:dare")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🔴 Dare task:\n{task}",
        reply_markup=reply_markup
    )

# ✅ When button click
async def answered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_clicking = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    parts = query.data.split(":")
    expected_id = int(parts[1])
    question_type = parts[2] if len(parts) > 2 else "unknown"

    if user_clicking != expected_id:
        await query.answer("❗ This is not for you!", show_alert=True)
        return

    # Database
    bot_user_id = get_or_create_user(user_clicking, username)
    save_answer(bot_user_id, question_type)

    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("🔁 Next questions: /truth /dare")

# 🔧 Bot applications
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("truth", truth))
app.add_handler(CommandHandler("dare", dare))
app.add_handler(CallbackQueryHandler(answered, pattern="^answered:"))

# 🧠 Making ready Base and running bot
init_db()
print("✅ Bot is running...")
app.run_polling()
