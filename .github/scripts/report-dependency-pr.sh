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
          "text": "*Repository:* \($repo)\nA new automated PR for dependency updates has been created and is ready for your review!\n\n<\($url)|Click here to view the Pull Request>"
        }
      }
    ]
  }' > pr-slack-payload.json

echo "Sending PR review request to Slack..."
curl -s -X POST -H 'Content-type: application/json' --data "@pr-slack-payload.json" "$SLACK_WEBHOOK_URL"
echo -e "\nDone!"
