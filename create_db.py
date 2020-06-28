import psycopg2
from psycopg2 import connect, extensions, sql
import argparse

def create_db(user,pw, db_name):
    # Falta ajuste para agregarlos desde cmd
    host = "localhost"

    conn = psycopg2.connect(
        host = host,
        user = user,
        password = pw)

    cur = conn.cursor()

    # get the isolation level for autocommit
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print ("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    conn.set_isolation_level( autocommit )
    sql_line = f"CREATE DATABASE {db_name};"
    cur.execute(sql_line)

    conn.commit()

    conn.close()
    cur.close()

    print('db created')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("postgres_user",
                        help="This is your username in Postgres",
                        type=str)

    parser.add_argument("postgres_password",
                        help="This is your password in Postgres",
                        type=str)
    
    parser.add_argument("db_name",
                        help="This is how you want to name the db",
                        type=str)

    args = parser.parse_args()
    create_db(args.postgres_user,args.postgres_password, args.db_name)
    