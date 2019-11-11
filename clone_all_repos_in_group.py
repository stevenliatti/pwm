#!/usr/bin/env python3

import sys
import json
import requests
import subprocess

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' <token> <group_id>')
    exit(1)

token = sys.argv[1]
group_id = sys.argv[2]

base_url = 'https://gitedu.hesge.ch/api/v4/'
params = {'simple': 'true', 'per_page': 100}
headers = {'PRIVATE-TOKEN': token}

repositories = requests.get(base_url + '/groups/' + group_id + '/projects', params=params, headers=headers).json()
if 'message' in repositories:
    print('Error retrieving repositories: ' + repositories['message'])
    exit(1)

for repo in repositories:
    repo_url = base_url + '/projects/' + str(repo['id']) + '/members'
    members = requests.get(repo_url, headers=headers).json()
    if 'message' in members:
        print('Error retrieving members: ' + members['message'])
        exit(1)

    ssh_url_to_repo = repo['ssh_url_to_repo']
    web_url = repo['web_url']
    members_names = ''

    for member in members:
        members_names += member['username'] + ', '

    print('Members: ' + members_names)
    print('Web url: ' + web_url)
    print('Cloning in "repositories/' + repo['path'] + '"\n')
    subprocess.run(["git", "clone", "-q", ssh_url_to_repo, "repositories/" + repo['path']])
