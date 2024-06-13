import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f'Привет, {user.first_name}!\n'
        'Я ваш справочник-бот. Пожалуйста, выберите раздел:',
        reply_markup=main_menu_keyboard()
    )


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton('Раздел 1')],
        [KeyboardButton('Раздел 2')],
        [KeyboardButton('Раздел 3')],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def handle_menu(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == 'Раздел 1':
        update.message.reply_text('Информация о Разделе 1: Lorem Ipsum...', reply_markup=sub_menu_keyboard())
    elif text == 'Раздел 2':
        update.message.reply_text('Информация о Разделе 2: Lorem Ipsum...', reply_markup=sub_menu_keyboard())
    elif text == 'Раздел 3':
        update.message.reply_text('Информация о Разделе 3: Lorem Ipsum...', reply_markup=sub_menu_keyboard())
    else:
        update.message.reply_text('Пожалуйста, выберите раздел из меню.', reply_markup=main_menu_keyboard())


def sub_menu_keyboard():
    keyboard = [
        [KeyboardButton('Опция 1')],
        [KeyboardButton('Опция 2')],
        [KeyboardButton('Главное меню')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def handle_sub_menu(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == 'Опция 1':
        update.message.reply_text('Информация о Опции 1: Lorem Ipsum...', reply_markup=sub_menu_keyboard())
    elif text == 'Опция 2':
        update.message.reply_text('Информация о Опции 2: Lorem Ipsum...', reply_markup=sub_menu_keyboard())
    elif text == 'Главное меню':
        update.message.reply_text('Вы вернулись в главное меню.', reply_markup=main_menu_keyboard())
    else:
        update.message.reply_text('Пожалуйста, выберите опцию из подменю.', reply_markup=sub_menu_keyboard())


def main() -> None:
    updater = Updater("токен")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_menu))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_sub_menu))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
