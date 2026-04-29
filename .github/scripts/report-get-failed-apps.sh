#!/bin/bash
set -e

FAILED_JOBS=$(gh api repos/"$GITHUB_REPOSITORY"/actions/runs/"$GITHUB_RUN_ID"/jobs \
  --jq '[.jobs[] | select(.conclusion == "failure" or .conclusion == "timed_out") | .name | sub("App deployment and testing \\("; "") | sub("\\)$"; "")] | join(", ")')

if [ -z "$FAILED_JOBS" ]; then
  WORKFLOW_STATUS="success"
else
  WORKFLOW_STATUS="failure"
fi

echo "failed_jobs=$FAILED_JOBS" >> "$GITHUB_OUTPUT"
echo "workflow_status=$WORKFLOW_STATUS" >> "$GITHUB_OUTPUT"
