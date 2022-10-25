import requests
from base64 import b64encode
from keys import toggl_setup

email_password = f"{toggl_setup['email']}:{toggl_setup['password']}"

data = requests.post(f'https://api.track.toggl.com/reports/api/v3/workspace/{toggl_setup["workspace_id"]}/search/time_entries',
        json='{"billable": False}',
        headers={'content-type': 'application/json', 'Authorization' : 'Basic %s' %  b64encode(bytes(email_password, 'ascii')).decode("ascii")})

print(data.text)
