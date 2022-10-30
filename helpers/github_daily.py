import requests
# from datetime import datetime
from pandas import to_datetime

from helpers.github_retriever import get_one_commit

def github_daily(github_setup, date):
    url = f'https://api.github.com/search/commits?q=author:kleczekr&order=desc&sort=committer-date&per_page=100'
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    auth = ('kleczekr', github_setup['OTP'])
    req = requests.get(url, headers=headers, auth=auth)
    date = to_datetime(date).tz_localize(None)
    commit_bucket = []
    for commit in req.json()['items']:
        committer = commit['committer']['login']
        commit_date = to_datetime(commit['commit']['author']['date']).tz_localize(None)
        if committer == 'kleczekr' and commit_date > date:
            message = commit['commit']['message']
            repo_name = commit['repository']['name']
            repo_url = commit['repository']['html_url']
            additions, deletions, total, filewise = get_one_commit(github_setup, commit['url'])
            dict_commit = {'committer': committer, 'date': commit_date, 'message': message, 'repo_name': repo_name, 'repo_url': repo_url, 'additions': additions, 'deletions': deletions, 'total': total, 'filewise': filewise}
            commit_bucket.append(dict_commit)
    return commit_bucket
