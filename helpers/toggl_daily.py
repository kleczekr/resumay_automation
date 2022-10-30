import requests
from base64 import b64encode
# import datetime
from pandas import to_datetime
import time

def toggl_daily(toggl_setup, tag_date, client_date, project_date, entry_date):
    since_unix = int(time.mktime(entry_date.timetuple()))
    auth_key = toggl_setup['token']
    string_token = f'{auth_key}:api_token'
    asciitoken = string_token.encode('ascii')
    b64token = b64encode(asciitoken)
    utf8token = b64token.decode('utf-8')

    tag_date = to_datetime(tag_date).tz_localize(None)
    client_date = to_datetime(client_date).tz_localize(None)
    project_date = to_datetime(project_date).tz_localize(None)
    entry_date = to_datetime(entry_date).tz_localize(None)

    raw_tags = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/tags',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    raw_tags = raw_tags.json()
    tags = []
    for tag in raw_tags:
        tag['at'] = to_datetime(tag['at']).tz_localize(None)
        if tag['at'] > tag_date:
            tags.append(tag)

    raw_clients = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/clients',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    raw_clients = raw_clients.json()
    clients = []
    for client in raw_clients:
        client['at'] = to_datetime(client['at']).tz_localize(None)
        if client['at'] > client_date:
            clients.append(client)

    raw_projects = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/projects',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    raw_projects = raw_projects.json()
    projects = []
    for project in raw_projects:
        project['at'] = to_datetime(project['at']).tz_localize(None)
        project['created_at'] = to_datetime(project['created_at'])
        if project['at'] > project_date:
            projects.append(project)

    raw_time_entries = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',
            params={"since":since_unix},
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    raw_time_entries = raw_time_entries.json()
    time_entries = []
    for entry in raw_time_entries:
        entry['start'] = to_datetime(entry['start']).tz_localize(None)
        entry['stop'] = to_datetime(entry['stop']).tz_localize(None)
        entry['at'] = to_datetime(entry['at']).tz_localize(None)
        if entry['at'] > entry_date:
            time_entries.append(entry)

    return tags, clients, projects, time_entries
