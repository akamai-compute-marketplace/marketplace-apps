# OpenLiteSpeed Node.js Quick Deploy App

OpenLiteSpeed is a high-performance, lightweight, open-source HTTP server. This deploys OpenLiteSpeed as both the web server and the Node.js application server on Ubuntu 24.04, serving a sample Node.js application over HTTPS with a Let's Encrypt certificate.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| OpenLiteSpeed | Latest | High-performance, lightweight, open-source HTTP server; also the Node.js application server via LSAPI |
| Node.js | Latest 26.x | JavaScript runtime, installed from the NodeSource apt repository (major pinned to 26.x) |
| LSPHP | Bundled | PHP runtime, selected automatically by the `openlitespeed` package; powers the WebAdmin console |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname | Assigns a hostname to the Linode based on the domain provided via UDF, or uses the default rDNS. For consistency, DNS and SSL configurations use the Hostname-generated `_domain` var. |
| Sudo User | Creates a limited `sudo` user from the UDF-supplied `username` and generates its password. Usernames containing illegal characters will cause the play to fail. |
| SSH Key | Assigns the account SSH key to the limited user. To add an SSH key to `root`, use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Secure SSH | Standard SSH hardening — writes to `/etc/ssh/sshd_config` to disable password auth and require public-key auth (applied only when `disable_root` is set to `Yes`). |
| Create DNS Record | Creates the DNS zone and A record via the Linode API when a `domain` and API `token_password` are supplied. |
| Update Packages | Performs standard apt update and upgrade actions as root. |
| UFW | Imports `ufw_rules.yml` (22, 80, 443, 7080) and enables the firewall. |
| Fail2Ban | Installs, activates, and enables the Fail2Ban service. |
| Certbot SSL | Issues the Let's Encrypt certificate using the **webroot** authenticator, served by OpenLiteSpeed itself. |
| Addons | Optional monitoring/observability exporters (`newrelic`, `node_exporter`, `mysqld_exporter`, `opentelemetry_collector`, `alloy`). |

## Post-Deployment

When the playbook finishes, the operator can:

- Browse to the sample Node.js application at `https://<domain-or-rdns>/`. It responds with
  `Hello World! From OpenLiteSpeed NodeJS`. Plain HTTP on port 80 redirects to HTTPS.
- Log in to the OpenLiteSpeed WebAdmin console at `https://<domain-or-rdns>:7080`, using the
  credentials below.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - WebAdmin username (`admin`) + password

### Replacing the sample application

The sample app lives at `/usr/local/lsws/Example/html/node/app.js` and is owned by
`nobody:nogroup`. To deploy your own application, place it in that directory (OpenLiteSpeed's Node
LSAPI looks for `app.js` by default) and restart the server:

```
sudo systemctl restart lshttpd
```

## Use our API

Customers can deploy OpenLiteSpeed Node.js through the Linode Marketplace or directly using the API. Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/), and substitute your own values for the defaults.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-2",
    "label": "openlitespeed-nodejs",
    "tags": [],
    "root_pass": "A_Secure_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 923031,
    "stackscript_data": {
        "user_name": "sudo_user",
        "disable_root": "No",
        "token_password": "A_Valid_API_Token",
        "subdomain": "examplesubdomain",
        "domain": "domain.tld",
        "soa_email_address": "email@domain.tld",
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
  --label openlitespeed-nodejs \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 923031 \
  --stackscript_data '{"user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","soa_email_address":"email@domain.tld","add_ons":"none"}'
```

## Resources

- [OpenLiteSpeed Documentation](https://docs.openlitespeed.org/)
- [OpenLiteSpeed Repository](https://github.com/litespeedtech/openlitespeed)
