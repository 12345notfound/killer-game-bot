# import sqlite3
import pandas as pd
from CustomException import *

# connection = sqlite3.connect("Killer_database.db")
# cursor = connection.cursor()


def ranking_table(id_game, name_user, connection):
    """Лидерборд"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM all_game WHERE id = ?", (id_game,))
    if cursor.fetchone() is None:
        raise IdError(f"id.{id_game} - не существует")

    cursor.execute("SELECT full_name, points FROM all_players WHERE id_game = ?", (id_game,))
    orders = cursor.fetchall()
    orders.sort(reverse=True, key=lambda x: x[1])

    df = pd.DataFrame({"player": [player[0] for player in orders], "points": [player[1] for player in orders]})

    df.to_excel(f'./downloads/ranking_{name_user}.xlsx', sheet_name='Ranking', index=False)

    return f"ranking_{name_user}.xlsx"


# ranking_table(20251, "sdf", cursor)


def order_table(id_game, name_user, connection):
    """Таблица заказов игроков"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM all_game WHERE id = ?", (id_game,))
    if cursor.fetchone() is None:
        raise IdError(f"id.{id_game} - не существует")

    cursor.execute("SELECT full_name, full_name_victim FROM all_players WHERE id_game = ?", (id_game,))
    orders = cursor.fetchall()
    orders.sort(key=lambda x: x[0])

    df = pd.DataFrame({"killer": [player[0] for player in orders], "victim": [player[1] for player in orders]})

    df.to_excel(f'./downloads/order_{name_user}.xlsx', sheet_name='Order', index=False)

    return f"order_{name_user}.xlsx"


# order_table(20251, "sdf", cursor)
# connection.close()
