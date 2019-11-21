#!/usr/bin/env python3

import sys
import requests
import string
import random

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <token> <project_id>")
    exit(1)

token = sys.argv[1]
project_id = sys.argv[2]

base_url = "https://githepia.hesge.ch/api/v4/projects"
params = {"simple": "true"}
headers = {"PRIVATE-TOKEN": token}

url = "%s/%s/forks" % (base_url, project_id)

repositories = requests.get(url, params=params, headers=headers).json()

alphabet = string.ascii_uppercase
for repo in repositories:
    print("create issue for repository %s" % repo['web_url'])
    issues_url = "%s/%s/issues" % (base_url, repo['id'])

    random_letter = random.choice(alphabet)
    alphabet.replace(random_letter, "")
    params = {
        "title": "You will be modeling the letter %s" % random_letter
    }
    new_issue = requests.post(issues_url, params=params, headers=headers)
