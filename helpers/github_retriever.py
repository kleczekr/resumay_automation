import requests
from pprint import pprint

def get_one_commit(github_setup, url):
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    auth = ('kleczekr', github_setup['OTP'])
    req = requests.get(url, headers=headers, auth=auth)
    pprint(req.json())

def github_retriever(github_setup):
    url = 'https://api.github.com/search/commits?q=author:kleczekr&order=desc&sort=committer-date&per_page=100'
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    auth = ('kleczekr', github_setup['OTP'])
    req = requests.get(url, headers=headers, auth=auth)
    # pprint(req.json())
    # pprint(req.json()['items'][0])
    get_one_commit(github_setup, req.json()['items'][0]['url'])
    # for item in req.json()['items']:
    #     print(item['commit']['author']['name'], item['commit']['author']['date'], item['comments_url'])

    print(len(req.json()['items']))
