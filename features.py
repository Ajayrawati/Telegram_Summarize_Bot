from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from summarize import summarize_text

import fitz  # PyMuPD
from url_handler import extract_text_from_url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
👋 **Hello! Welcome to SummarizeBot**  
I'm here to help you save time by turning long text, articles, or PDFs into short, clear summaries.

📌 **Here’s what I can do:**
• 📝 Paste or send me any **long text** – I’ll summarize it.
• 🌐 Share a **URL** – I’ll extract and summarize the content.
• 📄 Upload a **PDF** or TXT file – I’ll give you the key points.
• 🧠 Choose between **brief** (1-2 lines) or **detailed** summaries.
• 🌍 Translate summaries into different languages (soon).

🧪 Try sending:  
- A blog link  
- A news article  
- An essay  
- A PDF document  

Type `/help` for all available commands.

Let’s get started! 🚀
"""

    await update.message.reply_text(welcome_message, parse_mode="Markdown")



from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📝 Text", callback_data="summarize_text"),
            InlineKeyboardButton("🌐 URL", callback_data="summarize_url")
        ],
        [
            InlineKeyboardButton("📄 PDF", callback_data="summarize_pdf"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_summarize")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Please select the type of content you'd like to summarize:",
        reply_markup=reply_markup
    )


from telegram.ext import CallbackQueryHandler

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    context.user_data["input_type"] = data 
    if data == "summarize_text":
        await query.message.reply_text("📝 Please send the text you want to summarize.")
    elif data == "summarize_url":
        await query.message.reply_text("🌐 Please send the URL to summarize.")
    elif data == "summarize_pdf":
        await query.message.reply_text("📄 Please upload your PDF file.")
    elif data == "cancel_summarize":
        await query.message.reply_text("❌ Cancelled. You can type /start to begin again.")

def extract_pdf_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_type = context.user_data.get("input_type")

    if not input_type:
        await update.message.reply_text("❗ Please use /summarize first and select a content type.")
        return

    # 📝 If user chose text
    if input_type == "summarize_text":
        text = update.message.text
        summarized_text = summarize_text(text)
        await update.message.reply_text(f"✅ Summarized text:\n\n{summarized_text}")
        context.user_data.clear()

    # 🌐 If user chose URL
    elif input_type == "summarize_url":
        url = update.message.text
        print(f"[User URL]: {url}")
        text = extract_text_from_url(url)
        summarized_text = summarize_text(text)
        await update.message.reply_text(
                f"🧠 Summary:\n{summarized_text}"
            )


        context.user_data.clear()

    # 📄 If user chose PDF
    elif input_type == "summarize_pdf":
        doc = update.message.document
        if doc and doc.mime_type == "application/pdf":
            file = await doc.get_file()
            file_path = f"{doc.file_name}"
            await file.download_to_drive(file_path)
            try:
                text = extract_pdf_text(file_path)
                summarized_text = summarize_text(text)
            except Exception as e:
                await update.message.reply_text("⚠️ Failed to extract PDF content.")
                print(e)
            await update.message.reply_text(
                f"📥 Got your PDF: {doc.file_name}\n\n🧠 Summary:\n{summarized_text}"
            )


            os.remove(file_path)
            context.user_data.clear()
        else:
            await update.message.reply_text("❗ Please upload a valid PDF file.")








async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 **SummarizeBot Help Menu**

Here’s how you can use this bot to quickly get summaries of various content types:

🔹 **/start** — Start the bot and view the welcome message  
🔹 **/summarize** — Choose how you'd like to summarize (text, URL, or PDF)

---

🛠 **Features**:

1. **📝 Summarize Text**
   - Just type or paste long text after choosing this option
   - The bot will return a brief summary

2. **🌐 Summarize a URL**
   - Paste any article or blog link
   - The bot will fetch the content and summarize it

3. **📄 Summarize PDF**
   - Upload a PDF file
   - The bot will extract the text and generate a summary

---

🧠 More coming soon:
- Summary translation
- Summary tone/style control
- YouTube video summarizer

❓ For support or feedback, type a message here or reply with `/start` to begin again.

🔁 Ready to try? Type `/summarize` now!
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")
