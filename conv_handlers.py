import os

import telegram
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, InputFile

from Start_end_game import initializing_game, end_game
from Requests import *
from Update import update_point
from Table import ranking_table, order_table
from CustomException import *
import sqlite3

connection = sqlite3.connect("Killer_database.db")
cursor = connection.cursor()


async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет, этот бот создан, чтобы облегчить ведение игры \"Киллер\"\n"
                                    "Воспользуйтесь /help, чтобы узнать про возможности бота")


async def help(update, context):
    """Обработчик команды /help"""
    help_text = """
    Команды:
    /help - помощь по командам
    /stop - выход из диалогов
    /new_game - создание новой игры
    /delete_game - удаление игры
    /kill <убийца> - <жертва>    - регистрация убийства
    /fine <игрок> - <штраф> - <комментарий>     - регистрация штрафа
    /update_day - завершение игрового дня и перерасчет очков игроков
    /leaderboard - отправляет файл-таблицу с результатами игроков
    /orderboard - отправляет файл-таблицу с заказами игроков
    """
    await update.message.reply_text(help_text)


async def stop(update, context):
    """Обработчик выхода из диалога"""
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def new_game_state0(update, context):
    """Обработчик """
    await update.message.reply_text("Введите название новой игры")
    return 1


async def new_game_state1(update, context):
    context.chat_data['game_name'] = update.message.text.strip()
    await update.message.reply_text("Выберите (введите) ID (краткий номер) новой игры")
    return 2


async def new_game_state2(update: telegram.Update, context):
    # ----- вставить проверку уникальности имени игры -----
    id_str = update.message.text.strip()
    if not id_str.isdecimal():
        await update.message.reply_text("Введено не число, попробуйте снова")
        return 2
    id_int = int(id_str.lstrip('0'))
    context.chat_data['game_id'] = id_int
    await update.message.reply_text("Отправьте (формат?) файл со списком участников\n"
                                    "Формат: строки вида <ФИО/ФИ участника>,<класс участника>")
    return 3


async def new_game_state3(update: telegram.Update, context):
    get_file = await update.message.document.get_file()
    await get_file.download_to_drive(custom_path="downloads/temp.txt")
    file = open("downloads/temp.txt").readlines()
    os.remove('downloads/temp.txt')
    for line in file:
        line = line.strip().split(',')
    names = [elem[0] for elem in file]
    if len(set(names)) != len(names):  # есть повторы
        await update.message.reply_text("В списке участников есть одинаковые записи,"
                                        " отправьте исправленный список")
        return 3  # возврат в то же состояние

    game_info = {"name": context.chat_data["game_name"],
                 "start_day": str(update.message.date)[:10].replace('-', '.'),
                 "players": [{"full_name": elem[0], "class": elem[1]} for elem in file]
                 }
    initializing_game(game_info, connection)
    await update.message.reply_text("Игра создана!"
                                    " Для регистрации килла используйте /kill, для завершения дня /update_day")
    return ConversationHandler.END


async def delete_game_state0(update: telegram.Update, context):
    await update.message.reply_text("Введите id удаляемой игры")
    return 1


async def delete_game_state1(update: telegram.Update, context):
    game_id = update.message.text.strip()
    context.chat_data["delete_game_id"] = game_id
    await update.message.reply_text("Вы уверены, что хотите удалить эту игру?",
                                    reply_markup=ReplyKeyboardMarkup(["Да", "Нет"]))
    return 2


async def delete_game_state2(update: telegram.Update, context):
    text = update.message.text.strip()
    if text == "Нет":
        await update.message.reply_text("Операция удаления прервана.")
        return ConversationHandler.END
    try:
        end_game(context.chat_data["delete_game_id"], connection)
    except IdError as e:
        await update.message.reply_text(str(e.args[0]))
        return ConversationHandler.END
    await update.message.reply_text(f"Игра с id {context.chat_data['delete_game_id']} удалена")
    return ConversationHandler.END


async def register_kill(update: telegram.Update, context):
    """Обработчик регистрации килла"""
    text = update.message.text[5:].strip().split('-')
    killer, victim = text[0], text[1]
    # ----- к этому моменту в killer и target лежат соответственно киллер и жертва -----
    try:
        kill_commit({"name_killer": killer, "name_victim": victim}, connection)
        await update.message.reply_text(f"все окей, {killer} - {victim}")
    except (PlayerError, ImpossibleRequestError) as e:
        await update.message.reply_text(str(e.args[0]))


async def register_fine(update: telegram.Update, context):
    text = update.message.text[5:].strip().split('-')
    player, fine, comment = text[0], text[1], text[2]
    try:
        fine_commit({"name_player": player, "fine_point": fine, "comment": comment}, connection)
        await update.message.reply_text(f"Штраф записан: {text}")
    except PlayerError as e:
        await update.message.reply_text(str(e.args[0]))


# async def update_day(update: telegram.Update, context):
#     """Обработчик завершения дня и переподсчета очков
#     (команда /update_day)"""
#     game_id = update.message.text[10:].strip()
#     # ----- здесь нужно вызвать функцию для обновления дня с аргументом game_name -----
#     try:
#         update_point(game_id, cursor)
#         await update.message.reply_text("День успешно обновлен, используйте /leaderboard,"
#                                         " чтобы получить список очков игроков")
#     except IdError as e:
#         await update.message.reply_text(str(e.args[0]))


# async def leaderboard(update: telegram.Update, context):
#     """Обработчик создания лидерборда"""
#     game_id = update.message.text[11:].strip()
#     name_user = ...
#     # ----- здесь нужно вызвать функцию, которая возвращает файл с лидербордом
#     try:
#         filename = ranking_table(game_id, name_user, cursor)
#         await update.message.reply_document(filename)
#         os.remove(filename)
#     except IdError as e:
#         await update.message.reply_text(str(e.args[0]))


# async def orderboard(update: telegram.Update, context):
#     game_id = update.message.text[10:].strip()
#     name_user = ...
#     try:
#         filename = order_table(game_id, name_user, cursor)
#         await update.message.reply_document(filename)
#         os.remove(filename)
#     except IdError as e:
#         await update.message.reply_text(str(e.args[0]))
async def update_day_state0(update: telegram.Update, context):
    await update.message.reply_text("Введите id игры")
    return 1


async def update_day_state1(update: telegram.Update, context):
    game_id = update.message.text.strip()
    # ----- здесь нужно вызвать функцию для обновления дня с аргументом game_name -----
    try:
        update_point(game_id, connection)
        await update.message.reply_text("День успешно обновлен, используйте /leaderboard,"
                                        " чтобы получить список очков игроков")
    except IdError as e:
        await update.message.reply_text(str(e.args[0]))
    return ConversationHandler.END


async def leaderboard_state0(update: telegram.Update, context):
    await update.message.reply_text("Введите id игры")
    return 1


async def leaderboard_state1(update: telegram.Update, context):
    game_id = update.message.text.strip()
    name_user = update.effective_user.id
    try:
        filename = "downloads/" + ranking_table(game_id, f"{str(name_user)}_{game_id}", connection)
        await update.message.reply_document(document=open(filename, 'rb'))
        os.remove(filename)
    except IdError as e:
        await update.message.reply_text(str(e.args[0]))
    return ConversationHandler.END


async def orderboard_state0(update: telegram.Update, context):
    await update.message.reply_text("Введите id игры")
    return 1


async def orderboard_state1(update: telegram.Update, context):
    game_id = update.message.text.strip()
    name_user = update.effective_user.id
    try:
        filename = "downloads/" + order_table(game_id, f"{str(name_user)}_{game_id}", connection)
        await update.message.reply_document(document=open(filename, 'rb'))
        os.remove(filename)
    except IdError as e:
        await update.message.reply_text(str(e.args[0]))
    return ConversationHandler.END


def add_all_handlers(application):
    """Добавляет все обработчики диалогов"""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('kill', register_kill))
    application.add_handler(CommandHandler('fine', register_fine))
    # application.add_handler(CommandHandler('update_day', update_day))

    create_new_game_handler = ConversationHandler(
        entry_points=[CommandHandler('new_game', new_game_state0)],
        states={1: [CommandHandler('stop', stop), MessageHandler(filters.ALL, new_game_state1)],
                2: [CommandHandler('stop', stop), MessageHandler(filters.ALL, new_game_state2)],
                3: [CommandHandler('stop', stop), MessageHandler(filters.ALL, new_game_state3)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(create_new_game_handler)

    delete_game_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_game', delete_game_state0)],
        states={1: [CommandHandler('stop', stop), MessageHandler(filters.ALL, delete_game_state1)],
                2: [CommandHandler('stop', stop), MessageHandler(filters.ALL, delete_game_state2)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(delete_game_handler)

    leaderboard_handler = ConversationHandler(
        entry_points=[CommandHandler("leaderboard", leaderboard_state0)],
        states={1: [CommandHandler('stop', stop), MessageHandler(filters.ALL, leaderboard_state1)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(leaderboard_handler)

    orderboard_handler = ConversationHandler(
        entry_points=[CommandHandler("orderboard", orderboard_state0)],
        states={1: [CommandHandler('stop', stop), MessageHandler(filters.ALL, orderboard_state1)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(orderboard_handler)

    update_day_handler = ConversationHandler(
        entry_points=[CommandHandler("update_day", update_day_state0)],
        states={1: [CommandHandler('stop', stop), MessageHandler(filters.ALL, update_day_state1)]},
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(update_day_handler)
