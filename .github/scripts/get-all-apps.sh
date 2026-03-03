#!/usr/bin/env bash

set -e

APPS=$(find deployment_scripts -mindepth 1 -maxdepth 1 -type d | awk -F'/' '{print $2}' | sort -u | tr '\n' ',' | sed 's/,$//')

echo "Found apps in deployment_scripts: $APPS"

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