import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are a friendly AI tutor for students Class 1 to Class 12 in India.
- Answer ALL subjects: Math, Science, Physics, Chemistry, Biology, English, Hindi, History, Geography, Civics, Computer Science, Economics, Sanskrit
- Use SIMPLE language for Class 1-5, MEDIUM for Class 6-8, DETAILED for Class 9-12
- For Math: always show step-by-step solution
- For Science: use simple real-life examples
- Follow NCERT syllabus style
- Be encouraging, patient and friendly
- Match the class level of the student
End every answer with: Hope that helps! Ask me anything else"""

def ask_groq(user_message, user_name):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Student: {user_name}\nQuestion: {user_message}"}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = """🎓 Welcome to AI Study Helper! 100% Free 24/7

📚 Subjects: Math, Science, English, Hindi, Physics, Chemistry, Biology, History, Geography, Civics, Computer, Economics, Sanskrit

✅ Class 1 to Class 12
✅ NCERT Syllabus
✅ Available 24/7

👉 Example: I am in Class 10. Explain Newton laws

Lets start learning!"""
    await update.message.reply_text(welcome)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """📖 HOW TO USE:

Always mention your class first!

Math: Class 8 - Solve 3x + 6 = 18
Science: Class 7 - Explain photosynthesis
English: Class 9 - What is a metaphor?
Social: Class 6 - What is the water cycle?
Computer: Class 10 - What is HTML?

NCERT syllabus based!"""
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        answer = ask_groq(user_message, user_name)
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Sorry, please try again!")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is LIVE!")
    app.run_polling()

if __name__ == "__main__":
    main()
