import requests
from base64 import b64encode
from pprint import pprint
import datetime
from pandas import to_datetime
import time

today = datetime.date.today()
today_str = f'{today.strftime("%Y-%m-%d")}T00:00:00+00:00'
since_unix = int(time.mktime(datetime.datetime.strptime(today_str, "%Y-%m-%dT%H:%M:%S+00:00").timetuple()))

def toggl_retriever(toggl_setup):
    auth_key = toggl_setup['token']

    string_token = f'{auth_key}:api_token'
    asciitoken = string_token.encode('ascii')
    b64token = b64encode(asciitoken)
    utf8token = b64token.decode('utf-8')

    tags = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/tags',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    tags = tags.json()
    for tag in tags:
        # tag['at'] = datetime.datetime.strptime(tag['at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        tag['at'] = to_datetime(tag['at'])

    clients = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/clients',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    clients = clients.json()
    for client in clients:
        # client['at'] = datetime.datetime.strptime(client['at'], '%Y-%m-%dT%H:%M:%S+00:00')
        client['at'] = to_datetime(client['at'])

    projects = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/projects',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    projects = projects.json()
    for project in projects:
        # project['at'] = datetime.datetime.strptime(project['at'], '%Y-%m-%dT%H:%M:%S+00:00')
        project['at'] = to_datetime(project['at'])
        # project['created_at'] = datetime.datetime.strptime(project['created_at'], '%Y-%m-%dT%H:%M:%S+00:00')
        project['created_at'] = to_datetime(project['created_at'])

    time_entries = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',
            # params={"since":since_unix},
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    time_entries = time_entries.json()
    for entry in time_entries:
        # entry['start'] = datetime.datetime.strptime(entry['start'], '%Y-%m-%dT%H:%M:%S+00:00')
        entry['start'] = to_datetime(entry['start'])
        # entry['stop'] = datetime.datetime.strptime(entry['stop'], '%Y-%m-%dT%H:%M:%S+00:00')
        entry['stop'] = to_datetime(entry['stop'])
        # entry['at'] = datetime.datetime.strptime(entry['at'], '%Y-%m-%dT%H:%M:%S+00:00')
        entry['at'] = to_datetime(entry['at'])
    return tags, clients, projects, time_entries
