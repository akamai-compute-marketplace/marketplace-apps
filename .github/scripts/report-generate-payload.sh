#!/bin/bash
set -e

if [ "$WORKFLOW_STATUS" == "success" ]; then
  HEADER_TEXT="✅ Workflow Succeeded"
  FAILED_TEXT=""
else
  HEADER_TEXT="❌ Workflow Failed"
  FAILED_TEXT="*Failed Jobs:* ${FAILED_JOBS}"$'\n'
fi

jq -n \
  --arg status "$WORKFLOW_STATUS" \
  --arg header "$HEADER_TEXT" \
  --arg repo "$REPO_NAME" \
  --arg workflow "$WORKFLOW_NAME" \
  --arg failed "$FAILED_TEXT" \
  --arg url "$RUN_URL" \
  '{
    "text": "Workflow Result: \($status)",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": $header,
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Repository:* \($repo)\n*Workflow:* \($workflow)\n*Status:* `\($status)`\n\($failed)<\($url)|Click here to view the run details.>"
        }
      }
    ]
  }' > slack-payload.json

echo "Sending report to Slack..."
curl -s -X POST -H 'Content-type: application/json' --data "@slack-payload.json" "$SLACK_WEBHOOK_URL"
echo -e "\nDone!"
