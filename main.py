# full_60day_ielts_bot.py
# ПОВНА ВЕРСІЯ — встав TOKEN і запускай
import os
import json
import logging
import datetime
from datetime import timezone, date, time as dtime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== НАЛАШТУВАННЯ ======
# Встав свій токен сюди або встанови змінну середовища BOT_TOKEN
TOKEN = "8212213442:AAEmhJXvUl91-CJ8xCQ_PZOjw9tfrcUw1-o"
# Дата старту курсу — можеш змінити (YYYY, M, D)
START_DATE = date(2025, 9, 10)
# Файли для збереження підписників
SUBS_FILE = "subscribers.json"
# Час розсилки: 01:00 UTC ≈ 19:00 Alberta (MST) (перевір при зміні DST)
SEND_TIME_UTC = dtime(hour=1, minute=0, second=0, tzinfo=timezone.utc)
TOTAL_DAYS = 60

# ====== ЗАВДАННЯ (60 ДНІВ, короткі й практичні) ======
tasks = {
  1: "🎧 Listening: Cambridge sample Section 1\n✍️ Writing: 5 sentences about your city.",
  2: "📖 Reading: short BBC article\n🗣 Speaking: Describe your typical day (2 min).",
  3: "🎧 Listening: Cambridge sample Section 2\n✍️ Writing: 5 sentences about your home.",
  4: "📖 Reading: Wikipedia – read one page\n🗣 Speaking: Describe a friend (2 min).",
  5: "🎧 Listening: Cambridge sample Section 3\n✍️ Writing: 5 past-tense sentences.",
  6: "📖 Reading: short CNN piece\n🗣 Speaking: Talk about your favorite movie (2 min).",
  7: "🔁 Review: repeat week content + short Listening (15 min).",
  8: "🎧 Listening: Cambridge Section 4\n✍️ Writing: 5 future-tense sentences.",
  9: "📖 Reading: short news item\n🗣 Speaking: Describe your job (2 min).",
 10: "🎧 Listening: Cambridge 11 Section 1\n✍️ Writing: Photo description (5 sentences).",
 11: "📖 Reading: Wikipedia (2 pages)\n🗣 Speaking: Favorite food (2 min).",
 12: "🎧 Listening: Cambridge 11 Section 2\n✍️ Writing: 5 sentences using 'because'.",
 13: "📖 Reading: Reuters short\n🗣 Speaking: Describe your family (2 min).",
 14: "🔁 Review: timed Reading practice (20 min).",
 15: "🎧 Listening: Cambridge 11 Section 3\n✍️ Writing: 5 sentences with Present Perfect.",
 16: "📖 Reading: BBC medium article\n🗣 Speaking: Talk about your hobby (2 min).",
 17: "🎧 Listening: Cambridge 11 Section 4\n✍️ Writing: Short informal letter (5 sentences).",
 18: "📖 Reading: opinion piece (short)\n🗣 Speaking: Describe a memorable trip (2 min).",
 19: "🎧 Listening: Cambridge 12 Section 1\n✍️ Writing: 5 Past Continuous sentences.",
 20: "🔁 Mini-test: Listening (20 min) + short Writing (20 min).",
 21: "🎧 Listening: practice Section\n✍️ Grammar: Future Simple — 10 sentences.",
 22: "✍️ Writing Task 1: describe a chart (short)\n🗣 Speaking: Tell about your best friend.",
 23: "📖 Reading: academic excerpt (1 passage)\n📚 Vocab: learn 10 new words.",
 24: "🎧 Listening: practice test section\n✍️ Writing Task 2: short opinion essay (150 words).",
 25: "🗣 Speaking: Describe your last holiday (2 min)\n✍️ Grammar: conditionals — 10 sentences.",
 26: "📖 Reading: NG article (short)\n🎧 Listening: timed practice (20 min).",
 27: "🔁 Review: Speaking Part 2 practice — 2 min monologue.",
 28: "✍️ Writing Task 2: 'Should children use smartphones?'\n🎧 Listening: practice test.",
 29: "📖 Reading: academic passage\n🗣 Speaking: Talk about a challenge you overcame (2 min).",
 30: "🎧 Listening: Cambridge sample\n✍️ Writing Task 1: describe a table (short).",
 31: "📖 Reading: UK article\n🗣 Speaking: A skill you want to learn (2 min).",
 32: "🎧 Listening practice\n📚 Vocab: 10 more words.",
 33: "✍️ Writing Task 2: 'Is it better to study abroad?'\n📝 Grammar: reported speech — 10 examples.",
 34: "📖 Reading: academic excerpt\n🗣 Speaking: Talk about childhood memory (2 min).",
 35: "🎧 Listening: higher-level practice\n✍️ Writing Task 1: describe a process (short).",
 36: "🔁 Review: full Reading simulation (60 min or 1 passage timed).",
 37: "🗣 Speaking: Describe your job/career ambitions (2 min)\n✍️ Writing: short email to a friend.",
 38: "🎧 Listening practice (longer)\n📚 Vocab: 10 advanced words.",
 39: "✍️ Writing Task 2: 'Does money make you happy?'\n📖 Reading: related article.",
 40: "🎧 Listening practice + grammar: complex sentences (10 examples).",
 41: "✍️ Writing Task 1: line graph description (short)\n🗣 Speaking: Describe an invention.",
 42: "📖 Reading: longer BBC article\n🎧 Listening: timed section.",
 43: "📚 Vocab: 15 words + use them in sentences\n✍️ Writing: short opinion paragraph.",
 44: "🎧 Listening: practice section\n📝 Grammar: advanced tenses (10 examples).",
 45: "🔁 Review: Speaking Part 3 mock discussion (10–12 min).",
 46: "✍️ Writing Task 2: 'Should governments invest more in space?'\n🎧 Listening: practice.",
 47: "📖 Reading: academic passage\n🗣 Speaking: Describe a famous person (2 min).",
 48: "📚 Vocab + linking words practice\n✍️ Writing: short comparative paragraph.",
 49: "📖 Reading: full passage timed\n✍️ Writing Task 1: compare two charts (short).",
 50: "🔁 Review: full Listening test (simulate under time).",
 51: "📖 Reading: academic text\n🗣 Speaking: Describe your favorite season (2 min).",
 52: "✍️ Writing Task 2: 'Are exams fair? Discuss.'\n📚 Vocab: review learned words.",
 53: "🎧 Listening: Cambridge sample\n✍️ Writing: short summary (100 words).",
 54: "📝 Grammar: modals practice (10 sentences)\n🗣 Speaking: Talk about your goals (2 min).",
 55: "✍️ Writing Task 1: table description (short)\n🎧 Listening practice (section).",
 56: "📖 Reading: academic passage\n🗣 Speaking: Describe a famous historical event (2 min).",
 57: "✍️ Writing Task 2: 'Should public transport be free?'\n📚 Vocab: final review.",
 58: "🎧 Listening: Cambridge/full section\n📝 Grammar: linking words in writing (10 examples).",
 59: "🔁 Review: full Speaking mock + short Writing (150 words).",
 60: "🏁 FINAL: Full mock test — Listening, Reading, Writing, Speaking (simulate real timing)."
}

# ====== HELPERS: підписники ======
def load_subscribers():
    try:
        with open(SUBS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("subs", [])
    except Exception:
        return []

def save_subscribers(subs):
    with open(SUBS_FILE, "w", encoding="utf-8") as f:
        json.dump({"subs": subs}, f, ensure_ascii=False, indent=2)

def add_subscriber(chat_id):
    subs = load_subscribers()
    if chat_id not in subs:
        subs.append(chat_id)
        save_subscribers(subs)
        return True
    return False

def remove_subscriber(chat_id):
    subs = load_subscribers()
    if chat_id in subs:
        subs.remove(chat_id)
        save_subscribers(subs)
        return True
    return False

# ====== UTILS ======
def current_day_number():
    today = datetime.date.today()
    delta = (today - START_DATE).days + 1
    if delta < 1:
        return None
    if delta > TOTAL_DAYS:
        return None
    return int(delta)

def build_message_for(day_num):
    task = tasks.get(day_num, "Завдання ще не додане.")
    return f"📅 День {day_num} з {TOTAL_DAYS}\n\n{task}\n\n💡 Порада: дотримуйся таймінгу — Task1 ≈20 min, Task2 ≈40 min."

# ====== HANDLERS ======
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    added = add_subscriber(chat_id)
    if added:
        await update.message.reply_text("✅ Ти підписаний на щоденні завдання. Напиши /help для команд.")
    else:
        await update.message.reply_text("Ти вже підписаний. Щовечора отримуватимеш завдання.")

async def cmd_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    removed = remove_subscriber(chat_id)
    if removed:
        await update.message.reply_text("❌ Ти відписаний від щоденної розсилки.")
    else:
        await update.message.reply_text("Тебе не знайдено в підписниках.")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📘 Команди:\n"
        "/start — підписатися на щоденні завдання\n"
        "/stop — відписатися\n"
        "/today — отримати завдання на сьогодні\n"
        "/dayX — отримати завдання конкретного дня (наприклад /day5)\n"
        "/help — ця підказка\n"
    )
    await update.message.reply_text(text)

async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day = current_day_number()
    if day is None:
        await update.message.reply_text("Курс ще не почався або вже завершено.")
    else:
        await update.message.reply_text(build_message_for(day))

async def cmd_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        num = int(text.replace("/day", "").strip())
        if 1 <= num <= TOTAL_DAYS:
            await update.message.reply_text(build_message_for(num))
        else:
            await update.message.reply_text(f"Вкажи номер дня від 1 до {TOTAL_DAYS}.")
    except Exception:
        await update.message.reply_text("Використай формат /day<number> (наприклад /day7).")

# ====== DAILY SENDER ======
async def send_daily_job(context: ContextTypes.DEFAULT_TYPE):
    # This job runs at 01:00 UTC (approx 19:00 Alberta). It will send today's task to all subscribers.
    day = current_day_number()
    subs = load_subscribers()
    if day is None:
        logger.info("Daily job: курс ще не почався або завершено. Нічого не надсилаю.")
        return
    if not subs:
        logger.info("Daily job: немає підписників.")
        return
    message = build_message_for(day)
    success = 0
    fail = 0
    for cid in subs:
        try:
            await context.bot.send_message(chat_id=cid, text=message)
            success += 1
        except Exception as e:
            logger.warning(f"Failed to send to {cid}: {e}")
            fail += 1
    logger.info(f"Daily job: sent day {day} to {success} subscribers, failed {fail}.")

# ====== MAIN ======
def main():
    if not TOKEN or TOKEN.startswith("ВСТАВ_") :
        logger.error("Вставте свій Telegram BOT TOKEN у змінну TOKEN у цьому файлі.")
        return

    app = Application.builder().token(TOKEN).build()

    # handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("day", cmd_day))

    # scheduled daily job (01:00 UTC ≈ 19:00 Alberta). Use timezone-aware time
    app.job_queue.run_daily(send_daily_job, time=SEND_TIME_UTC, name="daily_ielts")

    logger.info("Bot started. Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
