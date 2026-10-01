# Langflow Quick Deploy App

Easypanel is a self-hosted server control panel and Platform-as-aService (PasaS) built on Docker. It lets you easily deploy and manage websites, apps, and databases via a user-friendly dashboard.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| Easypanel | latest  | Self-hosted server control panel |
| Docker CE | latest | Container runtime |

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
| Addons | Optional monitoring/observability exporters (`newrelic`, `node_exporter`, `mysqld_exporter`, `opentelemetry_collector`, `alloy`). |

## Post-Deployment

When the playbook finishes, the operator can:

- Browse to the app at `https://<domain-or-rdns>/` and sign in with the email address supplied as the SOA/Let's Encrypt email, and the generated password.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - Easypanel admin email + password

## Known Limitations

Custom domains require a paid Easypanel license. Without a license, hosted apps are reachable only at `<app>.<subdomain>.easypanel.host`. You can see the Easypanel Default Domain by navigating to `https://<domain-or-rdns>/settings/server/general`

## Use our API

Customers can deploy Easypanel through Akamai Compute [Quick Deploy Apps](https://cloud.linode.com/linodes/create/marketplace) or directly using the API. Before using the commands below, create an [API token](https://techdocs.akamai.com/linode-api/reference/get-started#create-a-personal-access-token) or configure [linode-cli](https://techdocs.akamai.com/linode-api/reference/cli), and substitute your own values for the defaults.

SHELL:
```
curl -H "Content-Type: application/json"
-H "Authorization: Bearer $TOKEN"
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-2",
    "label": "easypanel-us-southeast",
    "tags": [],
    "root_pass": "A_Secure_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 1008125,
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
linode-cli linodes create
  --image 'linode/ubuntu24.04'
  --region us-southeast
  --type g6-standard-2
  --label easypanel-us-southeast
  --root_pass A_Secure_Password
  --authorized_users user1
  --authorized_users user2
  --booted true
  --backups_enabled false
  --private_ip false
  --stackscript_id 1008125
  --stackscript_data '{"soa_email_address":"email@domain.tld","user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","add_ons":"none"}'
```

## Resources

- [Easypanel documentation](https://easypanel.io/docs)
