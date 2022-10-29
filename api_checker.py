# import requests
# from base64 import b64encode
# import pprint
from pymongo import MongoClient
import json
from bson import json_util


from helpers.toggl_retriever import toggl_retriever
from helpers.github_retriever import github_retriever
from keys import toggl_setup, github_setup, mongo_setup

# toggl_retriever(toggl_setup)
# github_retriever(github_setup, 1)
returns = 100
counter = 0
github_list = []
while returns > 0:
    bucket, returns = github_retriever(github_setup, counter)
    if len(bucket) > 0:
        github_list.extend(bucket)
    print(counter)
    counter += 1

toggl_tags, toggl_clients, toggl_projects, toggl_time_entries = toggl_retriever(toggl_setup)

github_json = json.dumps(github_list, default=json_util.default)
toggl_time_entries_json = json.dumps(toggl_time_entries, default=json_util.default)
toggl_tags_json = json.dumps(toggl_tags, default=json_util.default)
toggl_clients_json = json.dumps(toggl_clients, default=json_util.default)
toggl_projects_json = json.dumps(toggl_projects, default=json_util.default)

mongo_string = mongo_setup['url']

client = MongoClient(mongo_string)
db = client['resumay']
collection_github = db['github']
collection_toggl_time = db['toggl_time']
collection_toggl_tags = db['toggl_tags']
collection_toggl_clients = db['toggl_clients']
collection_toggl_projects = db['toggl_projects']

with open('github.txt', 'w') as f:
    for item in github_list:
        f.write("%s\n" % item)

collection_github.insert_many(github_list)
collection_toggl_time.insert_many(toggl_time_entries)
collection_toggl_tags.insert_many(toggl_tags)
collection_toggl_clients.insert_many(toggl_clients)
collection_toggl_projects.insert_many(toggl_projects)
