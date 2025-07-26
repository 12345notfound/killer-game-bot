import random
import sqlite3

connection = sqlite3.connect("Killer_database.db")
cursor = connection.cursor()


# info_game = {"id": int,
#         "name": str,
#         "start_day": ...,
#         "players": list}

# info_players = {"full_name": str,
#                 "class": int}

def initializing_game(info_game: dict, cursor):
    """инициализирует новую игру"""

    # Добавляет в список новую игру (если ее еще не существует)
    cursor.execute("SELECT id FROM all_game WHERE id = ?", (info_game["id"],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO all_game (id, name, start_day, status) VALUES (?, ?, ?, ?)',
                       (info_game["id"], info_game["name"], info_game["start_day"], 'Actively'))
    else:
        print(f'Игра c id {info_game["id"]} уже существует')
        return

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
            print(f"Игрок {player} уже существует")
            return

    connection.commit()


initializing_game({"id": 20251,
                   "name": "Старшие",
                   "start_day": "2025-08-13",
                   "players": [{"full_name": "ятченко кирилл вечаславович", "class": 11},
                               {"full_name": "русанов евгений васильевич", "class": 5},
                               {"full_name": "ятченко евгений васильевич", "class": 5},
                               {"full_name": "миронов евгений васильевич", "class": 5}]}, cursor)
initializing_game({"id": 20250,
                   "name": "Младшие",
                   "start_day": "2025-08-13",
                   "players": [{"full_name": "кравченко кирилл вечаславович", "class": 11},
                               {"full_name": "замоторин евгений васильевич", "class": 5}]}, cursor)

connection.close()
