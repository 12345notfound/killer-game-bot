import logging
from concurrent.futures import TimeoutError
import os

import telegram.error
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, InputMediaPhoto, MenuButtonCommands, MenuButton, ReplyKeyboardRemove, \
    MenuButtonWebApp, \
    InlineKeyboardButton, InlineKeyboardMarkup, MenuButton

from conv_handlers import add_all_handlers


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def main():
    BOT_TOKEN = '7711937878:AAHyDxJAasGUOq4q29nTftlrFCRJuHVMb1w'
    application = Application.builder().token(BOT_TOKEN).build()

    add_all_handlers(application)
    application.run_polling()


if __name__ == '__main__':
    main()