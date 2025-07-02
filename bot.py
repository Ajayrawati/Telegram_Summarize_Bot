from dotenv import load_dotenv
import os
import asyncio
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
import features


# Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")


# Async function to register slash commands
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "How to use the bot"),
        BotCommand("summarize", "Summarize text, URL, or PDF"),
    ])


# Main bot logic
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).post_init(set_commands).build()

    # Register handlers
    app.add_handler(CommandHandler("start", features.start))
    app.add_handler(CommandHandler("help", features.help_command))
    app.add_handler(CommandHandler("summarize", features.summarize))
    app.add_handler(CallbackQueryHandler(features.button_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.PDF, features.handle_user_input))

    app.run_polling()
