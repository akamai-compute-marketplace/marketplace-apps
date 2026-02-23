#!/usr/bin/env bash

set -e

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