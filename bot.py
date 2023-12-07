import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
# from telegram.ext import Filters, MessageHandler

from src.backend.config import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
new_locale =''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        chat_id = update.message.chat_id
        username = update.message.chat.first_name
        message_id = update.message.message_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        username = update.callback_query.message.chat.first_name
        message_id = update.callback_query.message.message_id
    
    await context.bot.delete_message(chat_id, message_id)
    await context.bot.send_message(chat_id, text=f"HI {username}")
        

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    user_message = update.message.text

    response_message = f"You sent: {user_message}"

    await context.bot.send_message(update.message.chat_id, response_message)

    
def main() -> None:
    # connection_check()
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
