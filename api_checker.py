import requests
from base64 import b64encode
import pprint

from helpers.toggl_retriever import toggl_retriever
from helpers.github_retriever import github_retriever
from keys import toggl_setup, github_setup

toggl_retriever(toggl_setup)
github_retriever(github_setup)
