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
new_locale = ''

userStorage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    username = update.effective_user.first_name

    await context.bot.delete_message(chat_id, message_id)
    await context.bot.send_message(chat_id, text=f"Привет <i><b>{username}</b></i>, я помогу тебе найти кроссовки по твоему запросу. Давай для начала выберем твой пол", parse_mode="HTML",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(
                                           text="Мужской", callback_data="men")],
                                       [InlineKeyboardButton(
                                           text="Женский", callback_data="women")],
                                   ]))


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    username = update.effective_user.first_name
    text_data = update.callback_query.data

    if text_data == "back":
        await context.bot.delete_message(chat_id, message_id)
        await context.bot.send_message(chat_id, text=f"Привет <i><b>{username}</b></i>, я помогу тебе найти кроссовки по твоему запросу. Давай для начала выберем твой пол", parse_mode="HTML",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton(
                                               text="Мужской", callback_data="men")],
                                           [InlineKeyboardButton(
                                               text="Женский", callback_data="women")],
                                       ]))


async def gender_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    username = update.effective_user.first_name

    await context.bot.delete_message(chat_id, message_id)
    text_data = update.callback_query.data

    if text_data == "men":
        context.chat_data[chat_id] = {'selected_gender': 'men'}
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, ты выбрали мужской пол.\n\nТеперь давай определимся какую именно пару мы будем с тобой искать\nP.S вот тебе пример (<i>Puma RS-Z 8.5 us</i>)", parse_mode="HTML")
    elif text_data == "women":
        context.chat_data[chat_id] = {'selected_gender': 'women'}
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, ты выбрали женский пол\n\nТеперь давай определимся какую именно пару мы будем с тобой искать\nP.S вот тебе пример (<i>Puma RS-Z 8.5 us</i>)", parse_mode="HTML")


async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    username = update.effective_user.first_name
    message_id = update.message.message_id
    userStorage[chat_id] = {'text': update.message.text,
                            '_list': update.message.text.lower(),
                            'selected_gender': context.chat_data.get(chat_id, {}).get('selected_gender', 'unknown')}

    await context.bot.delete_message(chat_id, message_id)
    await context.bot.send_message(chat_id, f"<i><b>{username}</b></i>, ищу {userStorage[chat_id]['text']}...", parse_mode="HTML")

    userStorage[chat_id]['res'], userStorage[chat_id]['url'] = await parsing(userStorage, chat_id)

    logger.info(userStorage[chat_id]['res'])

    if userStorage[chat_id]['res'] == False or not userStorage[chat_id]['res']:
        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, Не удалось найти кроссовки по вашему запросу: {userStorage[chat_id]['text']}", parse_mode="HTML")
    else:
        for idx, info in enumerate(userStorage[chat_id]['res']):
            name = info[0][0] if info[0] else "No Name"
            price = info[1][0] if info[1] else "No Price"

            image_path = f"./src/backend/gen_imgs/{userStorage[chat_id]['_list']}_{idx}_{userStorage[chat_id]['selected_gender']}_basketshop.jpg"

            await context.bot.send_photo(chat_id, photo=open(image_path, "rb"), caption=f"<b>Кроссовки: </b><i>{name}</i>\n\n <b>Цена:</b> <i>{price}</i>", parse_mode="HTML")

        await context.bot.send_message(chat_id, text=f"<i><b>{username}</b></i>, держи ссылку: {userStorage[chat_id]['url']}", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Назад", callback_data="back")]
            ]
        ))


def main() -> None:
    loop = asyncio.get_event_loop()
    connection_pool = loop.run_until_complete(connection.create_connection())
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(back, pattern="^(back)$"))
    application.add_handler(CallbackQueryHandler(
        gender_selection, pattern="^(men|women)$"))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_user_input))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("An error occurred: %s", e)
