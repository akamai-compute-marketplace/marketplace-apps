#!/usr/bin/env bash

set -e

CHANGED_FILES=$(git diff --name-only origin/main)

APPS=$(echo "$CHANGED_FILES" | awk -F'/' '/^(apps|deployment_scripts)\// {print $2}' | sort -u)
MATRIX=$(echo "$APPS" | tr '\n' ',' | sed 's/,$//')

echo "Found changes in the following app folders: $MATRIX"
echo "apps=$MATRIX" >>"$GITHUB_OUTPUT"
