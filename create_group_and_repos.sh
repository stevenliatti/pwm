#!/usr/bin/env bash

if [[ $# != 4 ]]; then
    echo "Usage: $0 <token> <group_name> <import_url> <repos_students>"
    exit 1
fi

token=$1
group_name=$2
import_url=$3
repos_students=$4

group=$(scripts/create_group.py $token $group_name)
group_id=$(echo $group | cut -d';' -f2)
printf "$group\n\n"

for line in $(cat $repos_students); do
    project_name=$(echo $line | cut -d';' -f1)
    students=$(echo $line | cut -d';' -f2)
    new_repo=$(scripts/create_repo_for_students.py $token $import_url $group_id $project_name $students)
    printf "$new_repo\n\n"
done
