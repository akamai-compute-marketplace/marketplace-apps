#!/bin/bash
set -e

jq -n \
  --arg repo "$REPO_NAME" \
  --arg url "$PR_URL" \
  '{
    "text": "New Dependency Updates PR ready for review!",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "📦 Dependency Updates Ready for Review",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Repository:* \($repo)\n*Pull Request:* <\($url)>"
        }
      }
    ]
  }' > pr-slack-payload.json

echo "Sending PR review request to Slack..."
curl -s -X POST -H 'Content-type: application/json' --data "@pr-slack-payload.json" "$SLACK_WEBHOOK_URL"
echo -e "\nDone!"