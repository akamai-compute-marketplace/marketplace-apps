#!/usr/bin/env bash

set -e

CHANGED_FILES=$(git diff --name-only origin/main)

APPS=$(echo "$CHANGED_FILES" | awk '
  /^apps\/[^\/]+\// {
    split($0, parts, "/"); apps[parts[2]] = 1
  }
  /^deployment_scripts\/[^\/]+\// {
    split($0, parts, "/"); apps[parts[2]] = 1
  }
  END {
    for (a in apps) print a
  }
' | sort -u)

if [ -z "$APPS" ]; then
	MATRIX="{\"include\":[]}"
else
	JSON_ARRAY="["
	SEP=""
	for app in $APPS; do
		JSON_ARRAY="${JSON_ARRAY}${SEP}{\"app\":\"$app\"}"
		SEP=","
	done
	JSON_ARRAY="${JSON_ARRAY}]"
	MATRIX="{\"include\":$JSON_ARRAY}"
fi

echo "Found changes in the following app folders: $MATRIX"
echo "matrix=$MATRIX" >>"$GITHUB_OUTPUT"
