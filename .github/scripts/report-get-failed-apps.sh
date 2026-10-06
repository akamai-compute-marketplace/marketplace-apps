#!/bin/bash
set -eo pipefail

JOBS_URL="repos/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}/attempts/${GITHUB_RUN_ATTEMPT}/jobs?per_page=100"

FAILED_JOB_NAMES='
  .jobs[]
  | select(.conclusion == "failure" or .conclusion == "timed_out")
  | .name
  | sub("^App deployment and testing \\("; "")
  | sub("\\)$"; "")
'

FAILED_JOBS=$(
  gh api --paginate "$JOBS_URL" --jq "$FAILED_JOB_NAMES" \
    | paste -sd ',' - \
    | sed 's/,/, /g'
)

if [ -z "$FAILED_JOBS" ]; then
  WORKFLOW_STATUS="success"
else
  WORKFLOW_STATUS="failure"
fi

echo "failed_jobs=$FAILED_JOBS" >> "$GITHUB_OUTPUT"
echo "workflow_status=$WORKFLOW_STATUS" >> "$GITHUB_OUTPUT"
