# 🎲 Telegram Truth & Dare Bot

This is a Telegram bot for playing the classic **Truth or Dare** game interactively within Telegram groups or private chats.

## 🚀 Features
- `/truth` — Sends a random **truth** question
- `/dare` — Sends a random **dare** task
- `/play` — Randomly chooses between truth or dare
- Only the user who received the question can click the ✅ "Answered" button
- All user answers are stored in a **SQLite** database
- Questions are automatically scraped from [Today.com](https://www.today.com) using `scraper.py`

## 📁 Project Structure
```
├── bot.py           # Main Telegram bot logic
├── database.py      # Database setup and logging
├── scraper.py       # Script to scrape questions from web
├── questions.json   # Stored truth & dare questions
├── requirements.txt # Python dependencies
└── .gitignore       # Prevents uploading sensitive and temp files
```

## ⚙️ Setup
Clone the repository and install dependencies:

```bash
git clone https://github.com/AlishGuluzade/truth-dare-bot.git
cd truth-dare-bot
pip install -r requirements.txt
```

Then, create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token
```

## ▶️ Run the bot
```bash
python bot.py
```

## 🖥️ Deployment
This bot is deployed and running as a `systemd` service on a **DigitalOcean** droplet, ensuring it stays online even when the terminal is closed.

## 👤 Author
Developed by **Alish Guluzade**  
GitHub: [@AlishGuluzade](https://github.com/AlishGuluzade)

---

🧪 This project is perfect for showcasing Python, Telegram Bot API, SQLite, and basic web scraping skills.
