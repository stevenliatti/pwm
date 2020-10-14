#!/usr/bin/env python3

import os
import requests
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "token", metavar="TOKEN", help="Create a token here: https://gitedu.hesge.ch/profile/personal_access_tokens")
parser.add_argument(
    "group_id", metavar="GROUP_ID", help="The group id (int) of the projects.")
parser.add_argument(
    "directory", metavar="DIRECTORY", help="Local directory where clone all repositories.")
parser.add_argument(
    "-u", "--until_date", help="Do a git checkout for all repositories at given date, format \"YYYY-MM-DD hh:mm\" (optional).")
args = parser.parse_args()

try:
    os.mkdir(args.directory)
except OSError:
    print("Creation of the directory '%s' failed, exit\n" % args.directory)
    exit(1)

base_url = 'https://gitedu.hesge.ch/api/v4/'
params = {'simple': 'true', 'per_page': 100}
headers = {'PRIVATE-TOKEN': args.token}

repositories = requests.get(base_url + '/groups/' + args.group_id +
                            '/projects', params=params, headers=headers).json()
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
    print('Cloning in "' + args.directory + '/' + repo['path'] + '"')

    subprocess.run(["git", "clone", "-q", ssh_url_to_repo,
                    args.directory + '/' + repo['path']])
    if args.until_date:
        commit_id = subprocess.check_output([
            "git", "rev-list", "-n", "1", "--before=\"" + args.until_date + "\"",
            "master"], cwd=args.directory + '/' + repo['path']).decode('utf-8').rstrip()
        subprocess.run(
            ["git", "checkout", "-q", str(commit_id)],
            cwd=args.directory + '/' + repo['path'])
        print("Checkout at " + str(commit_id) + "\n")
    else:
        print()
