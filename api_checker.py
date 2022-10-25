import requests
from base64 import b64encode
from keys import toggl_setup
import pprint
import os

email_password = f"{toggl_setup['email']}:{toggl_setup['password']}"
auth_key = toggl_setup['token']

string_token = f'{auth_key}:api_token'
asciitoken = string_token.encode('ascii')
b64token = b64encode(asciitoken)
utf8token = b64token.decode('utf-8')

data = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/tags',
headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
print('Tags:')
print(data.json())

data = requests.get(f'https://api.track.toggl.com/api/v9/workspaces/{toggl_setup["workspace_id"]}/clients',
        headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})
print('Clients:')
print(data.json())

data = requests.post(f'https://api.track.toggl.com/reports/api/v3/workspace/{toggl_setup["workspace_id"]}/search/time_entries',
        json={"end_date":"2022-10-26","previous_period_start":"2022-10-20","start_date":"2022-10-23",
            "client_ids": [61259608]},
        headers={'content-type': 'application/json', 'Authorization' : f'Basic {utf8token}'})

pprint.pprint(data.json())
