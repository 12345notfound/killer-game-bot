import sqlite3
import datetime
from CustomException import *

connection = sqlite3.connect("Killer_database.db")
cursor = connection.cursor()


def point_day(name_player, today_number_update, cursor):
    """Вычисляет очки за выживание"""

    cursor.execute("SELECT death_number_updates FROM all_players WHERE full_name = ?", (name_player,))
    death_number_updates = cursor.fetchone()[0]
    if death_number_updates is None:
        death_number_updates = today_number_update

    return 3 * death_number_updates


# kill = [name_victim, death]
def counter_kill_point(kills, death_number_updates_killer, today_number_update):
    """Расчитывает баллы за килы"""

    if death_number_updates_killer is None:
        death_number_updates_killer = today_number_update

    kill_point = 0
    for kill in kills:
        death_number_updates_killer_victim = kill[1]

        kill_point += 15
        kill_point += (death_number_updates_killer - death_number_updates_killer_victim)

    return kill_point


def update_death(id_game, cursor):
    """Обновляет даты смерти"""

    cursor.execute("SELECT * FROM all_kill WHERE id_game = ?", (id_game,))
    kills = cursor.fetchall()

    for kill in kills:
        cursor.execute('UPDATE all_players SET death_number_updates = ? WHERE full_name = ?', (kill[3], kill[2]))

    connection.commit()
    return


def update_fine_points(id_game, cursor):
    """Обновляет штрафные очки"""

    cursor.execute("SELECT * FROM fines WHERE id_game = ?", (id_game,))
    fines = cursor.fetchall()

    cursor.execute("SELECT full_name FROM all_players WHERE id_game = ?", (id_game,))
    players = list(map(lambda x: x[0], cursor.fetchall()))

    for player in players:
        fine_points = 0
        for fine in fines:
            if fine[1] == player:
                fine_points += fine[2]
        cursor.execute('UPDATE all_players SET fine_point = ? WHERE full_name = ?', (fine_points, player))

    connection.commit()
    return


# today - надо указать день публикации баллов
def update_point(id_game, cursor):
    """Обновляет все поинты игроков"""

    cursor.execute("SELECT * FROM all_game WHERE id = ?", (id_game,))
    if cursor.fetchone() is None:
        raise IdError(f"id.{id_game} - не существует")
    cursor.execute("SELECT number_updates FROM all_game WHERE id = ?", (id_game,))
    today_number_update = cursor.fetchone()[0] + 1

    update_death(id_game, cursor)
    update_fine_points(id_game, cursor)

    cursor.execute("SELECT * FROM all_kill WHERE id_game = ?", (id_game,))
    kills = cursor.fetchall()

    cursor.execute("SELECT * FROM all_players WHERE id_game = ?", (id_game,))
    players = cursor.fetchall()

    murder_graph = {}
    for player in players:
        murder_graph[player[0]] = {"kills": [], "death_number_updates": player[6], "point": 0}
    for kill in kills:
        murder_graph[kill[1]]["kills"].append(kill[2:4])

    def counter_point(name_player):
        """Подсчитывает баллы игрока"""

        full_point_player = 0
        # Очки за выживание
        full_point_player += point_day(name_player, today_number_update, cursor)
        # Очки за убийства
        kills_player = murder_graph[name_player]['kills']
        death_player = murder_graph[name_player]["death_number_updates"]
        full_point_player += counter_kill_point(kills_player, death_player, today_number_update)
        # Треть очков игроков
        for victim in kills_player:
            name_victim = victim[0]
            counter_point(name_victim)
            full_point_player += murder_graph[name_victim]['point'] // 3
        murder_graph[name_player]['point'] = full_point_player
        return

    for player in players:
        if murder_graph[player[0]]["death_number_updates"] is None:
            counter_point(player[0])

    for player in players:
        cursor.execute('UPDATE all_players SET points = ? WHERE full_name = ?',
                       (murder_graph[player[0]]['point'], player[0]))
        print(f"{player[0]}, {murder_graph[player[0]]['point']}")

    cursor.execute('UPDATE all_game SET number_updates = ? WHERE id = ?', (today_number_update, id_game))
    connection.commit()

    return


update_point(20251, cursor)
connection.close()
