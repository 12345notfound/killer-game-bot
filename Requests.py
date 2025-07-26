import sqlite3

connection = sqlite3.connect("Killer_database.db")
cursor = connection.cursor()


# kill = {"name_killer": str,
#         "name_victim": str,
#         "date": str}


def kill_commit(kill, cursor):
    """Комитит убийство"""

    name_killer, name_victim, date = kill["name_killer"], kill["name_victim"], kill["date"]

    cursor.execute("SELECT * FROM all_players WHERE full_name = ? OR full_name = ?", (name_killer, name_victim))
    if not cursor.fetchall() is None:
        cursor.execute("SELECT id_game FROM all_players WHERE full_name = ?", (name_killer,))
        id_game = cursor.fetchone()[0]
    else:
        print(f"Неверный запрос kill {name_killer, name_victim, date}: одного из людей не существует")
        return

    cursor.execute("SELECT * FROM all_kill WHERE name_victim = ?", (name_victim,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO all_kill (name_killer, name_victim, date, id_game) VALUES (?, ?, ?, ?)',
                       (name_killer, name_victim, date, id_game))
    else:
        print(f"Неверный запрос kill {name_killer, name_victim, date}: {name_victim} - убит")

    connection.commit()


kill_commit(
    {"name_killer": "ятченко кирилл вечаславович", "name_victim": "русанов евгений васильевич", "date": "2025-08-15"},
    cursor)


# fine = {"name_player": str,
#         "fine_point": int,
#         "comment": str}


def fine_commit(fine, cursor):
    """Комитит штраф"""

    name_player, fine_point, comment = fine["name_player"], fine["fine_point"], fine["comment"]

    cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_player,))
    if not cursor.fetchone() is None:
        cursor.execute("SELECT id_game FROM all_players WHERE full_name = ?", (name_player,))
        id_game = cursor.fetchone()[0]
    else:
        print(f"Неверный запрос fine ({name_player}): игрока не существует")
        return

    cursor.execute('INSERT INTO fines (name_player, fine_point, comment, id_game) VALUES (?, ?, ?, ?)',
                   (name_player, fine_point, comment, id_game))

    connection.commit()


fine_commit({"name_player": "ятченко кирилл вечаславович", "fine_point": -3, "comment": "потерял бумажку"}, cursor)

connection.close()
