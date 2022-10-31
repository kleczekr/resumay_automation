import psycopg2
from pymongo import MongoClient
import sys
sys.path.append('../')

from keys import postgres_setup, mongo_setup

conn = psycopg2.connect(database=postgres_setup['database'],
                        host=postgres_setup['host'],
                        user=postgres_setup['user'],
                        password=postgres_setup['password'],
                        port=postgres_setup['port'])

cursor = conn.cursor()

cursor.execute('SELECT version()')

version = cursor.fetchone()

print(version)

cursor.execute("""SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public'""")

rows = cursor.fetchall()

for row in rows:
    print(row[0])

cursor.execute('SELECT * FROM github')

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
