#!/bin/bash
set -e

jq -n \
  --arg repo "$REPO_NAME" \
  --arg current_branch "$CURRENT_BRANCH" \
  --arg target_branch "$TARGET_BRANCH" \
  --arg summary "$PR_TITLE" \
  --arg url "$PR_URL" \
  '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "✅ PR Merged",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Repo:* \($repo)\n*Current branch:* \($current_branch)\n*Target branch:* \($target_branch)\n*Summary:* \($summary)\n\($url)"
        }
      }
    ]
  }' > slack-payload.json

echo "Sending PR merge notification to Slack..."
curl -s -X POST -H 'Content-type: application/json' --data "@slack-payload.json" "$SLACK_WEBHOOK_URL"
echo -e "\nDone!"
