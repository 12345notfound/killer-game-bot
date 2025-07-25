import sqlite3


def kill_commit(name_killer, name_victim, date):
    """Комитит убийство"""

    connection = sqlite3.connect("Killer_database.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_killer,))
        id_killer = cursor.fetchall()[0][0]
        cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_victim,))
        id_victim = cursor.fetchall()[0][0]
    except IndexError:
        print(f"Неверный запрос kill {name_killer, name_victim, date}: одного из людей не существует")
        return

    cursor.execute("SELECT id_victim FROM all_kill WHERE id_victim = ?", (id_victim,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO all_kill (id_killer, id_victim, date) VALUES (?, ?, ?)',
                       (id_killer, id_victim, date))
    else:
        print(f"Неверный запрос kill {name_killer, name_victim, date}: {name_victim} - убит")

    connection.commit()
    connection.close()


kill_commit("ятченко кирилл вечаславович", "русанов евгений васильевич", "34.56.2025")


def fine_commit(name_player, fine, comment):
    """Комитит штраф"""

    connection = sqlite3.connect("Killer_database.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM all_players WHERE full_name = ?", (name_player,))
        id_player = cursor.fetchall()[0][0]
    except IndexError:
        print(f"Неверный запрос fine ({name_player}): игрока не существует")
        return

    cursor.execute('INSERT INTO fines (id_player, fine, comment) VALUES (?, ?, ?)',
                   (id_player, fine, comment))

    connection.commit()
    connection.close()


fine_commit("ятченко кирилл вечаславович", 3, "потерял бумажку")
