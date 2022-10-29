import requests
from base64 import b64encode
from pprint import pprint
import datetime
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

    clients = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/clients',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    clients = clients.json()

    projects = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/projects',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    projects = projects.json()

    time_entries = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',
            # params={"since":since_unix},
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})

    time_entries = time_entries.json()

    return tags, clients, projects, time_entries
