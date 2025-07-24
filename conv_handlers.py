import os

import telegram
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler


async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет и еще что-то")


async def help(update, context):
    """Обработчик команды /help"""
    help_text = ''
    await update.message.reply_text(help_text)


async def stop(update, context):
    """Обработчик выхода из диалога"""
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def new_game_state1(update, context):
    """Обработчик """
    await update.message.reply_text("Введите название новой игры")
    return 2


async def new_game_state2(update, context):
    context.chat_data['game_name'] = update.message.text.strip()
    await update.message.reply_text("Отправьте (формат?) файл со списком участников\n"
                                    "Формат: на каждой строке отдельно имя и фамилия")
    return 3


async def new_game_state3(update: telegram.Update, context):
    get_file = await update.message.document.get_file()
    await get_file.download_to_drive(custom_path="downloads/temp.txt")
    file = open("downloads/temp.txt").readlines()
    for line in file:
        line = line.strip()
    os.remove('downloads/temp.txt')
    # ----- к этому моменту в file лежит список участников,
    # а в context.chat_data['game_name'] - название игры -----

    return ConversationHandler.END


async def register_kill(update, context):
    """Обработчик регистрации килла"""
    text = update.message.text[5:].strip().split('-')
    killer, target = text[0], text[1]
    # ----- к этому моменту в killer и target лежат соответственно киллер и жертва -----
    await update.message.reply_text(f"все окей, {killer} - {target}")


def add_all_handlers(application):
    """Добавляет все обработчики диалогов"""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('kill', register_kill))

    create_new_game_handler = ConversationHandler(
        entry_points=[CommandHandler('new_game', new_game_state1)],
        states={2: [CommandHandler('stop', stop), MessageHandler(filters.ALL, new_game_state2)],
                3: [CommandHandler('stop', stop), MessageHandler(filters.ALL, new_game_state3)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(create_new_game_handler)

    # update_day_handler = ConversationHandler(
    #     entry_points=[],
    #     states={},
    #     fallbacks=[CommandHandler('stop', stop)]
    # )
    # application.add_handler(update_day_handler)
    #
    # leaderboard_handler = ConversationHandler(
    #     entry_points=[],
    #     states={},
    #     fallbacks=[CommandHandler('stop', stop)]
    # )
    # application.add_handler(leaderboard_handler)
    #
    # player_info_handler = ConversationHandler(
    #     entry_points=[],
    #     states={},
    #     fallbacks=[CommandHandler('stop', stop)]
    # )
    # application.add_handler(player_info_handler)
