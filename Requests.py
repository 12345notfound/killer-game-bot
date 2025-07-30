# import sqlite3
from CustomException import *


# connection = sqlite3.connect("Killer_database.db")
# cursor = connection.cursor()


# kill = {"name_killer": str,
#         "name_victim": str}


def kill_commit(kill, connection):
    """Комитит убийство"""

    cursor = connection.cursor()
    name_killer, name_victim = kill["name_killer"], kill["name_victim"]

    cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_killer,))
    result_1 = cursor.fetchall()
    cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_victim,))
    result_2 = cursor.fetchall()
    if result_2 and result_1:
        cursor.execute("SELECT id_game FROM all_players WHERE full_name = ?", (name_killer,))
        id_game = cursor.fetchone()[0]
    else:
        raise PlayerError(f"Неверный запрос kill {name_killer, name_victim}: одного из людей не существует")

    cursor.execute("SELECT * FROM all_kill WHERE name_victim = ?", (name_victim,))
    if cursor.fetchone() is None:
        cursor.execute("SELECT number_updates FROM all_game WHERE id = ?", (id_game,))
        date_number_updates = cursor.fetchone()[0]
        cursor.execute(
            'INSERT INTO all_kill (name_killer, name_victim, date_number_updates, id_game) VALUES (?, ?, ?, ?)',
            (name_killer, name_victim, date_number_updates, id_game))
    else:
        raise ImpossibleRequestError(f"Неверный запрос kill {name_killer, name_victim}: {name_victim} - убит")

    connection.commit()
    return


# kill_commit(
#     {"name_killer": "ятченко кирилл вечаславович", "name_victim": "русанов евгений васильевич"},
#     cursor)


# fine = {"name_player": str,
#         "fine_point": int,
#         "comment": str}


def fine_commit(fine, connection):
    """Комитит штраф"""

    cursor = connection.cursor()
    name_player, fine_point, comment = fine["name_player"], fine["fine_point"], fine["comment"]

    cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_player,))
    if not cursor.fetchone() is None:
        cursor.execute("SELECT id_game FROM all_players WHERE full_name = ?", (name_player,))
        id_game = cursor.fetchone()[0]
    else:
        raise PlayerError(f"Неверный запрос fine ({name_player}): игрока не существует")

    cursor.execute('INSERT INTO fines (name_player, fine_point, comment, id_game) VALUES (?, ?, ?, ?)',
                   (name_player, fine_point, comment, id_game))

    connection.commit()

# fine_commit({"name_player": "ятченко кирилл вечаславович", "fine_point": -3, "comment": "потерял бумажку"}, cursor)

# connection.close()
