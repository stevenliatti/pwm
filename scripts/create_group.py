#!/usr/bin/env python3

import os
import sys
import json
import requests
import subprocess

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' <token> <group_name> <visibility>')
    exit(1)

token = sys.argv[1]
group_name = sys.argv[2]
visibility = 'private'
if len(sys.argv) > 3:
    visibility = sys.argv[3]

base_url = 'https://gitedu.hesge.ch/api/v4/'
params = {'path': group_name, 'name': group_name, 'visibility': visibility}
headers = {'PRIVATE-TOKEN': token}

group = requests.post(base_url + '/groups', params=params, headers=headers).json()
if 'message' in group:
    print('Error in creating group: %s' % group)
    exit(1)

print("Group '" + group['name'] + "' with id '" + str(group['id']) + "' and visibility '" + group['visibility'] + "' available at '" + group['web_url'] + "';" + str(group['id']))
