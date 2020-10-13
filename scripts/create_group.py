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
    "group_name", help="The group name.")
parser.add_argument(
    "--visibility", help="Group visibility. By default private.")
args = parser.parse_args()

if args.visibility:
    visibility = args.visibility
else:
    visibility = 'private'

base_url = 'https://gitedu.hesge.ch/api/v4/'
params = {'path': args.group_name,
          'name': args.group_name, 'visibility': visibility}
headers = {'PRIVATE-TOKEN': args.token}

group = requests.post(base_url + '/groups',
                      params=params, headers=headers).json()
if 'message' in group:
    print('Error in creating group: %s' % group)
    exit(1)

print("Group '" + group['name'] + "' with id '" + str(group['id']) + "' and visibility '" +
      group['visibility'] + "' available at '" + group['web_url'] + "' ;" + str(group['id']))
