import logging
import datetime
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# =============== CONFIG ===============
TOKEN = os.getenv("BOT_TOKEN")  # 🔑 Твій Telegram Bot Token (вставити у Replit Secrets)
CHAT_ID = os.getenv("CHAT_ID")  # 🔑 Твій chat_id (для авто-розсилки)
SEND_HOUR = 19  # година відправки завдання
# =====================================

# Увімкнемо логування (для відладки)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Список завдань на 60 днів
tasks = {
    1: "🎯 Day 1:\nНапиши 5 речень про себе англійською.",
    2: "🎯 Day 2:\nПрослухай коротке відео англійською і занотуй 3 нових слова.",
    3: "🎯 Day 3:\nЗроби письмовий опис своєї роботи англійською (5-6 речень).",
    # ...
    60: "🎯 Day 60:\nПовне тренування: Speaking (2 хвилини), Writing (150+ слів), Listening (10 хвилин)."
}

# =============== Команди ===============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋 Я твій IELTS-батлер.\n"
        "Команди:\n"
        "/dayX (наприклад, /day5) – отримати завдання\n"
        "/today – сьогоднішнє завдання\n"
        "/help – список команд"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 Команди:\n"
        "/dayX – завдання певного дня\n"
        "/today – завдання на сьогодні\n"
        "/help – список команд"
    )

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        day_number = int(update.message.text.replace("/day", ""))
        task = tasks.get(day_number, "❌ Немає завдання для цього дня.")
        await update.message.reply_text(task)
    except ValueError:
        await update.message.reply_text("❌ Використовуй формат: /day5")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_date = datetime.date(2025, 9, 9)  # 👉 тут постав дату старту
    today_date = datetime.date.today()
    diff = (today_date - start_date).days + 1
    task = tasks.get(diff, f"✅ Тренування завершене! {diff} днів минуло.")
    await update.message.reply_text(task)

# =============== Авто-розсилка ===============
async def send_daily_task(application: Application):
    start_date = datetime.date(2025, 9, 9)  # 👉 та ж дата
    today_date = datetime.date.today()
    diff = (today_date - start_date).days + 1
    task = tasks.get(diff, "🎉 Всі 60 днів завершено!")
    if CHAT_ID:
        await application.bot.send_message(chat_id=CHAT_ID, text=task)

# =============== Запуск бота ===============
def main():
    app = Application.builder().token(TOKEN).build()

    # Команди
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("day", day))

    # Авто-розсилка
    scheduler = AsyncIOScheduler(timezone="Canada/Mountain")  # 🇨🇦 Alberta time
    scheduler.add_job(send_daily_task, "cron", hour=SEND_HOUR, args=[app])
    scheduler.start()

    logging.info("✅ Бот запущений")
    app.run_polling()

if __name__ == "__main__":
    main()
