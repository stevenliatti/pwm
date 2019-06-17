#!/usr/bin/env python3

import sys
import json
import requests
import subprocess

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' <token> <project_id>')
    exit(1)

token = sys.argv[1]
project_id = sys.argv[2]

base_url = 'https://gitedu.hesge.ch/api/v4/projects/'
params = {'simple': 'true'}
headers = {'PRIVATE-TOKEN': token}

repositories = requests.get(base_url + project_id + '/forks', params=params, headers=headers).json()

for repo in repositories:
    repo_url = base_url + str(repo['id']) + '/members'
    members = requests.get(repo_url, headers=headers).json()
    
    ssh_url_to_repo = repo['ssh_url_to_repo']
    web_url = repo['web_url']
    members_names = ''

    for member in members:
        if member['access_level'] > 20: # Access level greater than "Reporter"
            members_names += member['username'] + ', '

    print('Members: ' + members_names)
    print('Web url: ' + web_url)
    print('Cloning in "repositories/' + repo['namespace']['name'] + '"\n')
    subprocess.run(["git", "clone", "-q", ssh_url_to_repo, "repositories/" + repo['namespace']['name']])
