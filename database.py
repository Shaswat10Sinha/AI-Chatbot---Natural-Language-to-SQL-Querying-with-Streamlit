import sqlite3

def save_to_db(df, table_name, conn):
    """ Save uploaded DataFrame to SQLite database. """
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def get_table_names(conn):
    """ Retrieve table names from the SQLite database. """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]