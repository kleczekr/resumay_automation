import requests
from pprint import pprint
# from datetime import datetime
from pandas import to_datetime

def get_one_commit(github_setup, url):
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    auth = ('kleczekr', github_setup['OTP'])
    req = requests.get(url, headers=headers, auth=auth)
    additions = req.json()['stats']['additions']
    deletions = req.json()['stats']['deletions']
    total = req.json()['stats']['total']
    filewise = []
    for file in req.json()['files']:
        filename = file['filename']
        extension = filename.split('.')[-1]
        file_additions = file['additions']
        file_deletions = file['deletions']
        file_total = file['changes']
        dict_file = {'filename': filename, 'extension': extension, 'additions': file_additions, 'deletions': file_deletions, 'total': file_total}
        filewise.append(dict_file)
    return additions, deletions, total, filewise

def github_retriever(github_setup, page):
    url = f'https://api.github.com/search/commits?q=author:kleczekr&order=desc&sort=committer-date&per_page=100&page={page}'
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    auth = ('kleczekr', github_setup['OTP'])
    req = requests.get(url, headers=headers, auth=auth)
    commit_bucket = []
    for item in req.json()['items']:
        committer = item['committer']['login']
        if committer == 'kleczekr':
            date = to_datetime(item['commit']['author']['date'])
            message = item['commit']['message']
            repo_name = item['repository']['name']
            repo_url = item['repository']['html_url']
            additions, deletions, total, filewise = get_one_commit(github_setup, item['url'])
            dict_commit = {'committer': committer, 'date': date, 'message': message, 'repo_name': repo_name, 'repo_url': repo_url, 'additions': additions, 'deletions': deletions, 'total': total, 'filewise': filewise}
            print(repo_name)
            commit_bucket.append(dict_commit)
    results_length = len(req.json()['items'])
    return commit_bucket, results_length
