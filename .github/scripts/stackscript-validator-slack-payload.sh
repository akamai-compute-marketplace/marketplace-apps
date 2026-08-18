#!/usr/bin/env bash

set -euo pipefail

REPORT_TEXT=""

if [[ -f "$VALIDATOR_OUTPUT" ]]; then
  REPORT_TEXT=$(<"$VALIDATOR_OUTPUT")
fi

if [[ "$VALIDATOR_OUTCOME" == "success" ]] && [[ -z "$REPORT_TEXT" ]]; then
  jq -n \
    --arg repo "$REPO_NAME" \
    --arg url "$RUN_URL" \
    '{
      "text": "StackScript validator passed for \($repo)",
      "blocks": [
        {
          "type": "header",
          "text": {
            "type": "plain_text",
            "text": "✅ StackScript Validator Passed",
            "emoji": true
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "*Repository:* \($repo)\nNo failed StackScript checks were found.\n<\($url)|View workflow run>"
          }
        }
      ]
    }' > stackscript-validator-slack-payload.json
else
  if [[ -z "$REPORT_TEXT" ]]; then
    REPORT_TEXT="The validator did not produce any output."
  fi

  jq -n \
    --arg repo "$REPO_NAME" \
    --arg url "$RUN_URL" \
    --arg report "$REPORT_TEXT" \
    'def format_failure:
      if startswith("[ERROR] ") then
        capture("^\\[ERROR\\] (?<app>[^,]+), [^,]+, (?<ssid>[^:]+): (?<details>.*)$") |
        "• \(.app) - *ERROR*\n  StackScript ID: `\(.ssid)`\n  Details: \(.details)"
      elif startswith("[MISMATCH] ") then
        capture("^\\[MISMATCH\\] (?<app>[^,]+), [^,]+, (?<ssid>[^,]+)$") |
        "• \(.app) - *MISMATCH*\n  StackScript ID: `\(.ssid)`"
      else
        "• " + .
      end;

    {
      "text": "StackScript validator found failures for \($repo)",
      "blocks": [
        {
          "type": "header",
          "text": {
            "type": "plain_text",
            "text": "❌ StackScript Validator Failed",
            "emoji": true
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "*Repository:* \($repo)\nThe validator found failed checks:"
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": ($report | split("\n") | map(select(length > 0) | format_failure) | join("\n\n"))
          }
        },
        {
          "type": "context",
          "elements": [
            {
              "type": "mrkdwn",
              "text": "<\($url)|View workflow run>"
            }
          ]
        }
      ]
    }' > stackscript-validator-slack-payload.json
fi

curl --fail --silent --show-error \
  -X POST \
  -H 'Content-type: application/json' \
  --data "@stackscript-validator-slack-payload.json" \
  "$SLACK_WEBHOOK_URL"
