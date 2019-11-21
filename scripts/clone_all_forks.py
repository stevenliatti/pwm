#!/usr/bin/env python3

import os
import sys
import json
import requests
import subprocess

if len(sys.argv) < 4:
    print('Usage: ' + sys.argv[0] + ' <token> <project_id> <directory> <until_date>')
    exit(1)

directory = sys.argv[3]
try:
    os.mkdir(directory)
except OSError:
    print("Creation of the directory '%s' failed, exit\n" % directory)
    exit(1)

token = sys.argv[1]
project_id = sys.argv[2]

base_url = 'https://gitedu.hesge.ch/api/v4/projects/'
params = {'simple': 'true', 'per_page': 100}
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
            members_names += "'" + member['name'] + "' (" + member['username'] + '), '

    print('Members: ' + members_names)
    print('Web url: ' + web_url)
    print('Cloning in "' + directory + '/' + repo['namespace']['name'] + '"')

    subprocess.run(["git", "clone", "-q", ssh_url_to_repo, directory + '/' + repo['namespace']['name']])
    if len(sys.argv) > 4:
        until_date = sys.argv[4]
        commit_id = subprocess.check_output([
            "git","rev-list", "-n", "1", "--before=\"" + until_date + "\"",
            "master"], cwd=directory + '/' + repo['namespace']['name']).decode('utf-8').rstrip()
        subprocess.run(
            ["git", "checkout", "-q", str(commit_id)],
            cwd=directory + '/' + repo['namespace']['name'])
        print("Checkout at " + str(commit_id) + "\n")
    else:
        print()