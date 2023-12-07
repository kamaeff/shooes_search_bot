import logging
import asyncio
import telegram.ext.filters as filters

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler

from src.backend.config import TOKEN
from src.backend.DB import connection
from src.backend._search import parsing

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
new_locale =''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    username = update.effective_user.first_name
    
    await context.bot.delete_message(chat_id, message_id)
    await context.bot.send_message(chat_id, text=f"Привет <i><b>{username}</b></i>, я помогу тебе найти кроссовки по твоему запросу. Давай для начала выберем твой пол", parse_mode="HTML",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="Мужской", callback_data="male")],
                                       [InlineKeyboardButton(text="Женский", callback_data="female")],
                                   ]))

async def gender_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    username = update.effective_user.first_name
    
    await context.bot.delete_message(chat_id, message_id)
    selected_gender = update.callback_query.data
    
    context.user_data['selected_gender'] = selected_gender
    
    if selected_gender == "male":
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, ты выбрали мужской пол.\n\nТеперь давай определимся какую именно пару мы будем с тобой искать\nP.S вот тебе пример (<i>Puma RS-Z 8.5 us</i>)", parse_mode="HTML")
    elif selected_gender == "female":
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, ты выбрали женский пол\n\nТеперь давай определимся какую именно пару мы будем с тобой искать\nP.S вот тебе пример (<i>Puma RS-Z 8.5 us</i>)", parse_mode="HTML")

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    username = update.effective_user.first_name
    message_id = update.message.message_id
    user_input = update.message.text
    user_list = []
    selected_gender = context.user_data.get('selected_gender', 'unknown')

    await context.bot.delete_message(chat_id, message_id - 1)
    await context.bot.delete_message(chat_id, message_id)

    user_list = user_input.lower().split(' ')
    print(user_list)
    
    res, url = parsing(user_list, selected_gender)
    
    if res == False:
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, Не удалось найти кроссовки по вашему запросу: {url}", parse_mode="HTML")
    else:
      parsed_info = ""
      for item in res:
          parsed_info += f"Кроссовки : {item[0][0]}\n"
          parsed_info += f"Цена: {item[1][0]}\n"
          parsed_info += "-" * 40 + "\n"
          
      await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, Результаты запроса:\n\n{parsed_info}\nСсылка: {url}", parse_mode="HTML")
  
    context.user_data.clear()


def main() -> None:
    loop = asyncio.get_event_loop()
    connection_pool = loop.run_until_complete(connection.create_connection())
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(gender_selection, pattern="^(male|female)$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

