#!/usr/bin/env bash

set -e

echo "Current branch: $BRANCH"
echo "Target branch: $TARGET"

CHANGED_FILES=$(git diff --name-only origin/$TARGET)
APPS=$(echo "$CHANGED_FILES" | awk -F'/' '/^(apps|deployment_scripts)\// {print $2}' | sort -u | tr '\n' ',' | sed 's/,$//')

echo "Found changes in the following app folders: $APPS"

if [[ -z "$APPS" ]]; then
  echo "No app changes detected. Skipping Linode config search."
  echo "configs=[]" >>"$GITHUB_OUTPUT"
  exit 0
fi

IFS=',' read -ra apps <<< "$APPS"

json_output='['
for app in "${apps[@]}"; do
  if [[ -f "deployment_scripts/${app}/linode-config.sh" ]]; then
    json_output+="\"$app\","
  fi
done
json_output="${json_output%,}]"

echo "Found apps with existing Linode configs: $json_output"
echo "configs=$json_output" >>"$GITHUB_OUTPUT"