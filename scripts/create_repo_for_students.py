#!/usr/bin/env python3

import sys
import json
import requests
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "token", help="Create a token here: https://gitedu.hesge.ch/profile/personal_access_tokens")
parser.add_argument(
    "group_id", help="The group id (int) where to store the created new project.")
parser.add_argument(
    "emails", help="Emails list of students working in this project, separated by commas (email1,email2).")
parser.add_argument(
    "-n", "--name", help="The project name. If blank, take the first student name (from email) as name.")
parser.add_argument("-i", "--import_url",
                    help="Import the publicly accessible project by URL given here (optional).")
parser.add_argument("-x", "--expires_at",
                    help="Expiration date to kick off students from this project, at 00:00:00. YYYY-MM-DD format (optional).")
args = parser.parse_args()

base_url = 'https://gitedu.hesge.ch/api/v4'
headers = {'PRIVATE-TOKEN': args.token}

# split '@' in the case when project name = student's email
if args.name:
    name = args.name
else:
    name = args.emails.split('@')[0]

# Get students ids from their emails
users_emails = args.emails.split(',')
user_ids = []
for email in users_emails:
    user_requested = requests.get(
        base_url + '/users', params={'search': email}, headers=headers).json()
    if len(user_requested) == 0:
        print('No user %s found, operation aborted' % email)
        exit(1)
    user_id = user_requested[0]['id']
    user_ids.append(user_id)

# Create project from name, import_url (if given) and group_id
params = {'name': name, 'namespace_id': args.group_id, 'visibility': 'private'}
if args.import_url:
    params['import_url'] = args.import_url
project = requests.post(base_url + '/projects',
                        params=params, headers=headers).json()
if 'message' in project:
    print('Error in creating project: %s' % project)
    exit(1)
print("Project '" + project['name'] + "' at '" +
      project['web_url'] + "' created")

# Allow users with developer access level to push and merge on master
access_level = 30
params = {'name': 'master', 'push_access_level': str(
    access_level), 'merge_access_level': str(access_level)}
requests.post(base_url + '/projects/' +
              str(project['id']) + '/protected_branches', params=params, headers=headers).json()

# Add each student as project's developer (level 30)
for user_id in user_ids:
    params = {'user_id': user_id, 'access_level': access_level}
    if args.expires_at:
        params['expires_at'] = args.expires_at
    new_user = requests.post(base_url + '/projects/' + str(
        project['id']) + '/members', params=params, headers=headers).json()
    if 'message' in new_user:
        print('Error in adding user: %s' % new_user)
    else:
        out = ("Adding '" + new_user['name'] + "' (" + new_user['username'] + ") in '"
               + project['name'] + "' with access level: " + str(new_user['access_level']))
        if args.expires_at:
            out += ", expires at: " + new_user['expires_at']
        print(out)

# Do not forget : students have to add second remote in their local repositories for pulling last changes.
