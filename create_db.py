import psycopg2
from psycopg2 import connect, extensions, sql
from create_creds import read_creds_file


def create_db(user, pw, db_name):
    # Falta ajuste para agregarlos desde cmd
    host = "localhost"

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=pw)

    cur = conn.cursor()

    # get the isolation level for autocommit
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    conn.set_isolation_level(autocommit)
    sql_line = f"CREATE DATABASE {db_name};"
    cur.execute(sql_line)

    sql_line = "CREATE DATABASE test_db;"
    cur.execute(sql_line)

    conn.commit()

    conn.close()
    cur.close()

    print('db created')


if __name__ == "__main__":
    creds = read_creds_file()
    create_db(creds['postgres_user'],
              creds['postgres_password'], creds['db_name'])
