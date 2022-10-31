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

cursor.execute(
    """CREATE TABLE IF NOT EXISTS github (
        id SERIAL PRIMARY KEY,
        committer TEXT NOT NULL,
        message TEXT NOT NULL,
        repo_name TEXT NOT NULL,
        repo_url TEXT NOT NULL,
        additions INT NOT NULL,
        deletions INT NOT NULL,
        total INT NOT NULL,
        date TIMESTAMP NOT NULL
    )""")

cursor.execute(
        """CREATE TABLE IF NOT EXISTS github_filewise (
            id SERIAL PRIMARY KEY,
            github_id INT,
            filename TEXT NOT NULL,
            extension TEXT NOT NULL,
            additions INT NOT NULL,
            deletions INT NOT NULL,
            total INT NOT NULL,
            CONSTRAINT FK_github_id FOREIGN KEY (github_id) REFERENCES github (id)
        )""")

client = MongoClient(mongo_setup['url'])
db = client['resumay']
collection = db['github']

all_commits = collection.find()

for commit in all_commits:
    cursor.execute(
        """INSERT INTO github (committer, message, repo_name, repo_url, additions, deletions, total, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (commit['committer'], commit['message'], commit['repo_name'], commit['repo_url'], commit['additions'], commit['deletions'], commit['total'], commit['date']))

    cursor.execute("""SELECT id FROM github WHERE committer = %s AND message = %s AND repo_name = %s AND repo_url = %s AND additions = %s AND deletions = %s AND total = %s AND date = %s""",
        (commit['committer'], commit['message'], commit['repo_name'], commit['repo_url'], commit['additions'], commit['deletions'], commit['total'], commit['date']))

    github_id = cursor.fetchone()[0]

    for file in commit['filewise']:
        cursor.execute(
            """INSERT INTO github_filewise (github_id, filename, extension, additions, deletions, total)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (github_id, file['filename'], file['extension'], file['additions'], file['deletions'], file['total']))
    print('Inserted commit: ' + commit['message'])

cursor.close()
