import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# إعداد المفاتيح
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# رسالة الترحيب
WELCOME_MESSAGE = """
👋 مرحباً بك في البوت الذكي!

🤖 هذا البوت هو نموذج ذكاء اصطناعي متطور مبني باستخدام تقنيات OpenAI (ChatGPT).

🧠 يمكنك سؤاله عن أي شيء وسيرد عليك فوراً بإجابات ذكية ومفيدة.

💡 تم تطوير هذا البوت بواسطة: *عبدالرحمن جمال عبدالرب العطاس*
"""

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')

# الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"]
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("حدث خطأ أثناء الاتصال بـ OpenAI: " + str(e))

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن...")
    app.run_polling()
