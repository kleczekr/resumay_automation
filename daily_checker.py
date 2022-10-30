from pymongo import MongoClient

from helpers.toggl_daily import toggl_daily
from helpers.github_daily import github_daily
from keys import toggl_setup, github_setup, mongo_setup

mongo_string = mongo_setup['url']

# Connect to MongoDB
client = MongoClient(mongo_string)
db = client['resumay']
collection_github = db['github']
collection_toggl_time = db['toggl_time']
collection_toggl_projects = db['toggl_projects']
collection_toggl_tags = db['toggl_tags']
collection_toggl_clients = db['toggl_clients']

last_github = collection_github.find_one(sort=[("date", -1)])
last_toggl_time = collection_toggl_time.find_one(sort=[("at", -1)])
last_toggl_projects = collection_toggl_projects.find_one(sort=[("at", -1)])
last_toggl_tags = collection_toggl_tags.find_one(sort=[("at", -1)])
last_toggl_clients = collection_toggl_clients.find_one(sort=[("at", -1)])

last_github_date = last_github['date']
last_toggl_time_date = last_toggl_time['at']
last_toggl_projects_date = last_toggl_projects['at']
last_toggl_tags_date = last_toggl_tags['at']
last_toggl_clients_date = last_toggl_clients['at']

print("Last Github date: ", last_github_date)
print("Last Toggl time date: ", last_toggl_time_date)
print("Last Toggl projects date: ", last_toggl_projects_date)
print("Last Toggl tags date: ", last_toggl_tags_date)
print("Last Toggl clients date: ", last_toggl_clients_date)

github = github_daily(github_setup, last_github_date)
toggl_tags, toggl_clients, toggl_projects, toggl_time_entries = toggl_daily(toggl_setup,
        last_toggl_tags_date, last_toggl_clients_date, last_toggl_projects_date, last_toggl_time_date)

if github:
    collection_github.insert_many(github)

if toggl_tags:
    collection_toggl_tags.insert_many(toggl_tags)

if toggl_clients:
    collection_toggl_clients.insert_many(toggl_clients)

if toggl_projects:
    collection_toggl_projects.insert_many(toggl_projects)

if toggl_time_entries:
    collection_toggl_time.insert_many(toggl_time_entries)
