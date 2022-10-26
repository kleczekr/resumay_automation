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
    print('Tags:')
    pprint(tags.json())

    clients = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/clients',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    print('Clients:')
    pprint(clients.json())

    projects = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/projects',
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    print('Projects:')
    pprint(projects.json())

    # time_entries = requests.post(f'https://api.track.toggl.com/reports/api/v3/workspace/{toggl_setup["workspace_id"]}/search/time_entries',
    #         json={"end_date":"2022-10-26","previous_period_start":"2022-10-20","start_date":"2022-10-23"},
    #         headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
    # print('Time Entries:')
    # pprint(time_entries.json())

    time_entries_alternate = requests.get('https://api.track.toggl.com/api/v9/me/time_entries',
            params={"since":since_unix},
            headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})

    print('Time entries alternate:')
    pprint(time_entries_alternate.json())
