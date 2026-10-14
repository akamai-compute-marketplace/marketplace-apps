# StackScripts

Keeps the Linode StackScripts in sync with the deploy scripts on `main`.

For every `deployment_scripts/linode-marketplace-<app>/<app>-deploy.sh` it fetches the StackScript named in the
`# STACKSCRIPT_ID:` header and compares the content. Results go to Slack. If anything differs, the workflow
waits for approval and then pushes the deploy scripts to those StackScripts.

## Workflow (`.github/workflows/stackscript-validator.yml`)

Runs weekly (Wednesday 09:00 UTC), on pushes to `main` that change `deployment_scripts/**`, and manually.

1. **validate** compares all apps and posts the results to Slack. If there are mismatches the message asks
   "Do you want to fix N StackScripts?" and links to the run.
2. **update** runs only if there were mismatches. It waits for approval in the `stackscript_production`
   environment, re-checks each app and updates the ones that still differ.

| Secret | Used by |
|---|---|
| `SLACK_WEBHOOK_URL` | validate & update |
| `STACKSCRIPT_API_TOKEN` | update only |

## Statuses

| Status | Meaning |
|---|---|
| `MATCH` | Same content |
| `MISMATCH` | Content differs; fixed by the update job |
| `MISSING_ID` | No `# STACKSCRIPT_ID:` header in the deploy script |
| `NOT_FOUND` | StackScript with that ID does not exist |
| `ERROR` | Linode API request failed |
| `UPDATED` / `FAILED` | Result of an update |

## Running locally

```bash
cd .github/scripts
pip install -r stackscripts/requirements.txt
python -m stackscripts validate
```

Without `SLACK_WEBHOOK_URL` nothing is sent to Slack; results are printed to the log.
`update` writes to production StackScripts, so run it through the workflow.

## Code structure

```
.github/scripts/stackscripts/
├── README.md
├── requirements.txt
├── __main__.py                      # parses arguments, runs a command
├── config.py                        # Config: settings from environment variables
├── exceptions.py                    # StackScriptJobError and subclasses
├── commands/                        # entry points, one class per command
│   ├── base_command.py              #   BaseCommand: run(), crash reporting, job outputs
│   ├── validate_command.py          #   ValidateCommand
│   └── update_command.py            #   UpdateCommand
├── services/                        # business logic
│   ├── deploy_script_reader.py      #   DeployScriptReader: deploy scripts from the repo
│   ├── stackscript_validator.py     #   StackScriptValidator: compares with Linode
│   └── stackscript_updater.py       #   StackScriptUpdater: pushes mismatches to Linode
├── clients/                         # external services
│   ├── linode_client.py             #   LinodeClient: get / update a StackScript
│   └── slack_client.py              #   SlackClient: post to the webhook
├── models/                          # data objects
│   ├── deploy_script.py             #   DeployScript
│   └── result.py                    #   Result, Status
└── reporting/                       # human-readable output
    ├── result_table.py              #   ResultTable: plain-text table
    └── slack_message_builder.py     #   SlackMessageBuilder: Slack Block Kit messages
```
