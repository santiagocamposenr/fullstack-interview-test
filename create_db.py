import psycopg2
from psycopg2 import connect, extensions, sql

# Falta ajuste para agregarlos desde cmd
host = "localhost"
user = "postgres"
pw = "postgres"

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

cur.execute('''CREATE DATABASE github_db;''')

conn.commit()

conn.close()
cur.close()

print('done')