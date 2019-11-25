#!/usr/bin/env python3

import sys
import json
import requests
import subprocess

if len(sys.argv) < 6:
    print('Usage: ' + sys.argv[0] + ' <token> <import_url> <group_id> <project_name> <student1,student2,...,studentN> <expires_at>')
    exit(1)

token = sys.argv[1]
import_url = sys.argv[2]
group_id = sys.argv[3]
project_name = sys.argv[4]

base_url = 'https://gitedu.hesge.ch/api/v4'
headers = {'PRIVATE-TOKEN': token}

# Get students ids from their usernames
users_names = sys.argv[5].split(',')
user_ids = []
for username in users_names:
    user_requested = requests.get(base_url + '/users', params={'username': username}, headers=headers).json()
    if len(user_requested) == 0:
        print('No user %s found, operation aborted' % username)
        exit(1)
    user_id = user_requested[0]['id']
    user_ids.append(user_id)

# Create project from name, basis and group given
params = {'name': project_name, 'import_url': import_url, 'namespace_id': group_id, 'visibility': 'private'}
project = requests.post(base_url + '/projects', params=params, headers=headers).json()

if 'message' in project:
    print('Error in creating project: %s' % project)
    exit(1)
print("Project '" + project['name'] + "' at '" + project['web_url'] + "' created")

# Allow users with developer access level to push and merge on master
access_level = 30
params = {'name': 'master', 'push_access_level': str(access_level), 'merge_access_level': str(access_level)}
requests.post(base_url + '/projects/' + str(project['id']) + '/protected_branches', params=params, headers=headers).json()

# Add each student as project's developer (level 30)
for user_id in user_ids:
    params = {'user_id': user_id, 'access_level': access_level}
    if len(sys.argv) > 6:
        expires_at = sys.argv[6]
        params['expires_at'] = expires_at
    new_user = requests.post(base_url + '/projects/' + str(project['id']) + '/members', params=params, headers=headers).json()

    if 'message' in new_user:
        print('Error in adding user: %s' % new_user)
    else:
        print(
            "Adding '" + new_user['name'] + "' (" + new_user['username'] + ") in '"
            + project['name'] + "' with access level: " + str(new_user['access_level'])
            + ", expires at: " + new_user['expires_at'])

# Do not forget : students have to add second remote in their local repositories for pulling last changes.
