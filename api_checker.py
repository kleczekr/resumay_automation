import requests
from base64 import b64encode
import pprint

from helpers.toggl_retriever import toggl_retriever
from keys import toggl_setup

toggl_retriever(toggl_setup)

