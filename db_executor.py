import sqlite3
import os


def init_base(connection_string="DB.db"):
    if not connection_string or not os.path.exists(os.path.join(os.path.dirname(__file__), connection_string)):
        raise OSError("DB file is not located!")

    connection = sqlite3.connect(connection_string, check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    tablenames = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print([t['name'] for t in tablenames])
    return connection, tablenames


def get_sql_code(connection, tablename: str):
    cursor = connection.cursor()
    sql_code = cursor.execute(f"SELECT sql FROM sql_master WHERE type='table' AND name='{tablename}'").fetchone()
    if not sql_code:
        raise Exception("No such table or code!")
    return sql_code
