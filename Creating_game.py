import sqlite3


# info_game = {"id": int,
#         "name": str,
#         "start_day": ...,
#         "players": list}

# info_players = {"full_name": str,
#                 "class": int}

def initializing_game(info_game: dict):
    """инициализирует новую игру"""

    connection = sqlite3.connect("Killer_database.db")
    cursor = connection.cursor()

    # Добавляет в список новую игру (если ее еще не существует)
    cursor.execute("SELECT id FROM all_game WHERE id = ?", (info_game["id"],))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO all_game (id, name, start_day, status) VALUES (?, ?, ?, ?)',
                       (info_game["id"], info_game["name"], info_game["start_day"], 'Actively'))

    # Добавляет новых игроков (если их еще нет)
    for player in info_game["players"]:
        cursor.execute("SELECT full_name FROM all_players WHERE full_name = ?",
                       (" ".join(player["full_name"]).lower(),))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO all_players (full_name, class_player, id_game) VALUES (?, ?, ?)',
                           (" ".join(player["full_name"]).lower(), player["class"], info_game["id"]))

    connection.commit()
    connection.close()


initializing_game({"id": 20251,
                   "name": "Старшие",
                   "start_day": "23.05.2025",
                   "players": [{"full_name": ["Ятченко", "Кирилл", "Вечаславович"], "class": 11},
                               {"full_name": ["Русанов", "Евгений", "Васильевич"], "class": 5}]})
initializing_game({"id": 20250,
                   "name": "Младшие",
                   "start_day": "23.05.2025",
                   "players": [{"full_name": ["Кравченко", "Кирилл", "Вечаславович"], "class": 11},
                               {"full_name": ["Замоторин", "Евгений", "Васильевич"], "class": 5}]})
