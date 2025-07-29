import random
import sqlite3
from CustomException import *

connection = sqlite3.connect("Killer_database.db")
cursor = connection.cursor()


# info_game = {"id": int,
#         "name": str,
#         "players": list}

# info_players = {"full_name": str,
#                 "class": int}

def initializing_game(info_game: dict, cursor):
    """инициализирует новую игру"""

    # Добавляет в список новую игру (если ее еще не существует)
    cursor.execute("SELECT id FROM all_game WHERE id = ?", (info_game["id"],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO all_game (id, name, number_updates) VALUES (?, ?, ?)',
                       (info_game["id"], info_game["name"], 0))
    else:
        raise IdError(f'Игра c id {info_game["id"]} уже существует')

    # Добавляет новых игроков (если их еще нет)
    random.shuffle(info_game["players"])
    for i in range(len(info_game["players"])):
        player = info_game["players"][i]
        victim = info_game["players"][(i + 1) % (len(info_game["players"]))]
        cursor.execute("SELECT * FROM all_players WHERE full_name = ?",
                       (player["full_name"],))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO all_players (full_name, class_player, id_game, full_name_victim) VALUES (?, ?, ?, ?)',
                (player["full_name"], player["class"], info_game["id"], victim["full_name"]))
        else:
            raise PlayerError(f"Игрок {player} уже существует")

    connection.commit()
    return


initializing_game({"id": 20251,
                   "name": "Старшие",
                   "players": [{"full_name": "ятченко кирилл вечаславович", "class": 11},
                               {"full_name": "русанов евгений васильевич", "class": 5},
                               {"full_name": "ятченко евгений васильевич", "class": 5},
                               {"full_name": "миронов евгений васильевич", "class": 5}]}, cursor)
initializing_game({"id": 20250,
                   "name": "Младшие",
                   "players": [{"full_name": "кравченко кирилл вечаславович", "class": 11},
                               {"full_name": "замоторин евгений васильевич", "class": 5}]}, cursor)


def end_game(id_game, cursor):
    """Удаление всех данных об игре"""
    cursor.execute("SELECT id FROM all_game WHERE id = ?", (id_game,))
    if cursor.fetchone() is None:
        raise IdError(f'Игра c id {id_game} не существует, операция удаления прервана')

    cursor.execute('DELETE FROM all_game WHERE id = ?', (id_game,))
    cursor.execute('DELETE FROM all_players WHERE id_game = ?', (id_game,))
    cursor.execute('DELETE FROM all_kill WHERE id_game = ?', (id_game,))
    cursor.execute('DELETE FROM fines WHERE id_game = ?', (id_game,))

    connection.commit()
    return


# end_game(20251, cursor)

connection.close()
