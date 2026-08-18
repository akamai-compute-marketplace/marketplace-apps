# Stackscript Validator

## About

An integrity checker that compares the MD5 hash between Linode's Quick Deploy Apps and what's in the Linode API.

### Requirements

1. Install Python dependancies.
```bash
python3 -m venv env
source env/bin/activate
pip install pip -U
pip install -r requirements.txt
```
 
 ---

### Usage

The script is straight forward to use. It uses Python's Argparse library so when in doubt issue `--help`.

```
usage: Stackscript Checkum Validator [-h] (--show-all | --show-error | --show-mismatch | --show-failed | --show-match) [--table] [--text] [-u USERNAME] [-b BRANCH] [-r REPO]

Peformed MD5 checks on Github and backend deploy scripts.

optional arguments:
  -h, --help            show this help message and exit
  --show-all            Show all apps status
  --show-error          Show apps that have errors when fetching deployment script.
  --show-mismatch       Show apps with failed MD5 checks.
  --show-failed         Show apps with errors or failed MD5 checks.
  --show-match          Show apps that passed MD5 checks.

Report Format:
  --table               Output in table format
  --text                Output in text format

GitHub:
  -u USERNAME, --username USERNAME
                        Github user name
  -b BRANCH, --branch BRANCH
                        Github branch
  -r REPO, --repo REPO  Github repository
```

### Compare Branch Stackscript with Linode API

By default the script compares the deployment stackscript from the `akamai-compute-marketplace` user `main` branch. To compare changes from your branch just use the `-u USERNAME` and `-b BRANCH` params.

```bash
python3 stackscript-validator.py -u n0vabyte -b integrity-check --show-all
```

### Report Types

The script uses Rich to generate a table report. There are 5 types of reports that can be generated.

1. Show everything

To show all stackscript check status use the `--show-all` flag. This will display stackcripts that have `errors`, `mismatched` and `matched` statuses.

2. Show Errors

Using the `--show-error ` flag will display applications that failed for one reason or another. Deploy scripts that have bad `# STACKSCRIPT_ID:` values will fall under this category. Maybe the stackscript doesn't exist. This is a good filter if you just want to see those that failed.

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                   GitHub                   ┃ Stackscript ┃ MD5                                         ┃ Stackscript ID ┃                                                     Status                                                      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│        linode-marketplace-benchkit         │    ERROR    │ linode-marketplace-benchkit:                │ None           │ {"errors": [{"reason": "A StackScript with this ID does not exist or you do not have permission to view it."}]} │
│                                            │             │ 455b5ed83cecc3e4c8023bc6d2fa73ba            │                │                                                                                                                 │
├────────────────────────────────────────────┼─────────────┼─────────────────────────────────────────────┼────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
```

3. Show failed

The `--show-failed` flag combines the `--show-error` and `--show-mismatch` reports. It displays applications with either a deployment script error or a failed MD5 check.

4. Show MD5 mismatch

The `--show-mismatch` will display applications that failed the integrity check. This means that what's in Github and the Linode API do not match.

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃                GitHub                 ┃                   Stackscript                   ┃ MD5                                              ┃ Stackscript ID ┃  Status  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│      linode-marketplace-aapanel       │                aaPanel One-Click                │ linode-marketplace-aapanel:                      │ 869129         │ MISMATCH │
│                                       │                                                 │ 8d08cbe54c8bfe94845ece86c3083346                 │                │          │
│                                       │                                                 │                                                  │                │          │
│                                       │                                                 │ aaPanel One-Click:                               │                │          │
│                                       │                                                 │ 0648f5995b9fc73e80b3d70bf1b214fb                 │                │          │
├───────────────────────────────────────┼─────────────────────────────────────────────────┼──────────────────────────────────────────────────┼────────────────┼──────────┤
```

5. Show MD5 Match

To only view applications that passed the MD5 checks we can use the `--show-match` flag. Ideally this all deploy script checks should fall under this report type.

### Output Formats

This script is meant to be run locally by a user to check Stackscript hashes but also by other CLI tools. The default output format is table which utilizes the Python's Rich library. Passing `--text` to the CLI will output the results with a table:

Command:
```shell
python3 stackscript-validator.py -u n0vabyte -b update/add-stackscriptid --repo marketplace-clusters --show-all --text
```
Output:
```output
[MISMATCH] linode-marketplace-apache-cassandra, c070651aeb01acdb038dc2e058087c14, 1350845
[MISMATCH] linode-marketplace-apache-spark, f253a4cffab727e6cf4784679b62de7a, 1403818
[MISMATCH] linode-marketplace-couchbase, b29cc1f4baaf04846ae5549b4e5689d6, 1366191
[MISMATCH] linode-marketplace-elk, a260c9e7c525892c31166fd612eaaaaf, 1966222
[MISMATCH] linode-marketplace-galera, ad3c4e410df172fb4350636dc2e215e1, 1088136
[MISMATCH] linode-marketplace-glusterfs, c084057ffef638f4ba069d2ed3357ddd, 1350783
[MISMATCH] linode-marketplace-jitsi, 7542cffcc8f8798b01f1c8771e1eb709, 1350733
[MISMATCH] linode-marketplace-kafka, dc92b97208f9da8a71c5ee1391cc06fe, 1377657
[MISMATCH] linode-marketplace-nomad-client, 2a8da01c2f3c435352de35c0bb2abdfd, 1226545
[ERROR] linode-marketplace-nomad, 66367f7786d2fad85daa8aa9f56bdec5, None: {"errors": [{"reason": "A StackScript with this ID does not exist or you do not have permission to view it."}]}
[MISMATCH] linode-marketplace-postgresql, 105cb083ccc961fd1260b4e8d061e2de, 1068726
[MISMATCH] linode-marketplace-redis, ef418cb1f88749a20cd9e8dd2c6d8a63, 1132204
```