# Langflow Quick Deploy App

[Langflow](https://docs.langflow.org/) is an open-source, Python-based, customizable framework for building AI applications. It supports important AI functionality like agents and the Model Context Protocol (MCP), and it doesn't require you to use specific large language models (LLMs) or vector stores.

The visual editor simplifies prototyping of application workflows, enabling developers to quickly turn their ideas into powerful, real-world solutions. 

This Quick Deploy App deploys Langflow on Ubuntu 24.04 via Docker Compose (Langflow + PostgreSQL), behind nginx with a Let's Encrypt certificate and native superuser login.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| Langflow | latest  | Open-source visual framework for building AI agents and workflows |
| PostgreSQL | 18    | Relational database — Langflow's backing store |
| Nginx    | 1.24    | Web server / reverse proxy |
| Docker CE + Compose v2 | latest | Container runtime + orchestration |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname | Assigns a hostname to the Linode based on the domain provided via UDF, or uses the default rDNS. For consistency, DNS and SSL configurations use the Hostname-generated `_domain` var. |
| Sudo User | Creates a limited `sudo` user from the UDF-supplied `username` and generates its password. Usernames containing illegal characters will cause the play to fail. |
| SSH Key | Writes a UDF-supplied SSH pubkey to `/home/$username/.ssh/authorized_keys`. To add an SSH key to `root`, use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Secure SSH | Standard SSH hardening — writes to `/etc/ssh/sshd_config` to disable password auth and require public-key auth (applied only when `disable_root` is set). |
| Update Packages | Performs standard apt update and upgrade actions as root. |
| UFW | Imports `ufw_rules.yml` (22, 80, 443) and enables the firewall. PostgreSQL (5432) is not exposed. |
| Fail2Ban | Installs, activates, and enables the Fail2Ban service. |
| Docker | Installs Docker CE (used to run the Langflow + PostgreSQL Compose project). |
| Certbot SSL | Handles SSL/TLS certificate issuance via Let's Encrypt against nginx. |
| Addons | Optional monitoring/observability exporters (`newrelic`, `node_exporter`, `mysqld_exporter`, `opentelemetry_collector`, `alloy`). |

## Post-Deployment

When the playbook finishes, the operator can:

- Browse to the app at `https://<domain-or-rdns>/` and log in as `admin`.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - App URL
  - Langflow admin username + password
  - PostgreSQL user + password + database name
- On the canvas, drag and drop components from the left panel onto the board and connect them into a flow. Running a flow that calls an LLM or embeddings provider requires you to add your own provider API key (e.g. OpenAI) in the relevant component or under **Settings → Global Variables**. See the [Langflow Quickstart](https://docs.langflow.org/get-started-quickstart) for more information on getting started.

## Use our API

Customers can deploy Langflow through Akamai Compute [Quick Deploy Apps](https://cloud.linode.com/linodes/create/marketplace) or directly using the API. Before using the commands below, create an [API token](https://techdocs.akamai.com/linode-api/reference/get-started#create-a-personal-access-token) or configure [linode-cli](https://techdocs.akamai.com/linode-api/reference/cli), and substitute your own values for the defaults.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-2",
    "label": "langflow-us-southeast",
    "tags": [],
    "root_pass": "A_Secure_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 00000,
    "stackscript_data": {
        "soa_email_address": "email@domain.tld",
        "user_name": "sudo_user",
        "disable_root": "No",
        "token_password": "A_Valid_API_Token",
        "subdomain": "examplesubdomain",
        "domain": "domain.tld",
        "add_ons": "none"
    }
}' https://api.linode.com/v4/linode/instances
```

CLI:
```
linode-cli linodes create \
  --image 'linode/ubuntu24.04' \
  --region us-southeast \
  --type g6-standard-2 \
  --label langflow-us-southeast \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"soa_email_address":"email@domain.tld","user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","add_ons":"none"}'
```

## Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [Langflow Quickstart](https://docs.langflow.org/get-started-quickstart)
- [Langflow Repository](https://github.com/langflow-ai/langflow)
