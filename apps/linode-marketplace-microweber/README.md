# Microweber Quick Deploy App

[Microweber](https://microweber.org) is an open-source drag-and-drop CMS and e-commerce website
builder built on Laravel, aimed at users who want to compose pages, blogs, and online shops with
live edit rather than code. This Marketplace App deploys Microweber v2.0.20 on Ubuntu 24.04 as a
classic LAMP stack (Apache + mod_php + MariaDB), with the browser setup wizard eliminated via the
upstream CLI installer, a version-pinned and sha256-verified install artifact, automatic HTTPS via
Let's Encrypt, and native admin login as the auth layer.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| Microweber | 2.0.20 | Drag-and-drop CMS and e-commerce website builder (Laravel-based); install zip is version-pinned and sha256-verified |
| Apache   | 2.4.58 | Web server (mod_php), single vhost, HTTP→HTTPS and canonical-host redirects |
| PHP      | 8.3.6  | Ubuntu 24.04 distro PHP with Microweber's required extensions (no third-party PPA) |
| MariaDB  | 10.11.14 | Database server; root uses socket auth, app user is scoped to the app database |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname | Assigns a hostname to the Linode based on the domain provided via UDF, or uses the default rDNS. For consistency, DNS and SSL configurations use the Hostname-generated `_domain` var. |
| DNS Record | Creates a DNS A record via the Linode API when a domain and API token are provided via UDF. |
| Sudo User | Creates a limited `sudo` user from the UDF-supplied `username` and generates its password. Usernames containing illegal characters will cause the play to fail. |
| SSH Key | Writes the account's SSH pubkey(s) to `/home/$username/.ssh/authorized_keys`. To add an SSH key to `root`, use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Secure SSH | Standard SSH hardening — disables password auth and root login (applied only when `disable_root` is set). |
| Update Packages | Performs standard apt update and upgrade actions as root. |
| UFW | Allows 22, 80, 443/tcp and enables the firewall with a default-deny policy. MariaDB (3306) is not exposed. |
| Fail2Ban | Installs, activates, and enables the Fail2Ban service. |
| Secure MySQL | Generates the MariaDB root password and hardens the installation (removes anonymous users and the test database). |
| Certbot SSL | Handles TLS certificate issuance via Let's Encrypt against Apache (`webserver_stack: lamp`), with HTTP→HTTPS redirect. |
| Addons | Optional monitoring/observability exporters (`newrelic`, `node_exporter`, `mysqld_exporter`, `opentelemetry_collector`, `alloy`). |

## Post-Deployment

When the playbook finishes, the operator can:

- Browse the site at `https://<domain-or-rdns>/` and log in to the admin panel at
  `https://<domain-or-rdns>/admin` (username `admin`, password from the credentials file).
  There is no setup wizard — the site is fully installed, and the installer endpoint
  (`/install`) returns 404.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - MariaDB root password
  - Microweber database name, user, and password
  - Microweber admin username, password, and email
- Start building: the deploy seeds default content and activates the bundled **Big** template —
  use Live Edit from the admin panel to compose pages, or set up the shop under
  admin → Shop. Templates can be switched in admin → Design. See the
  [Microweber user documentation](https://microweber.org/docs) for first steps.

<!-- REVIEW: confirm the docs URL renders a real user guide (microweber.org/docs) — swap for
     https://microweber.com/help or the current upstream docs home if not. -->

## Use our API

Customers can deploy Microweber through the Linode Marketplace or directly using the API. Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/), and substitute your own values for the defaults.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-2",
    "label": "microweber-occ-us-southeast",
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
        "admin_email": "admin@domain.tld",
        "mw_db_user": "microweber",
        "mw_db_name": "microweber",
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
  --label microweber-occ-us-southeast \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"soa_email_address":"email@domain.tld","admin_email":"admin@domain.tld","mw_db_user":"microweber","mw_db_name":"microweber","user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","add_ons":"none"}'
```

<!-- REVIEW: replace stackscript_id 00000 with the real published StackScript ID once the app
     is live in the Marketplace. -->

## Resources

- [Microweber Website](https://microweber.org)
- [Microweber Documentation](https://microweber.org/docs)
- [Microweber Repository](https://github.com/microweber/microweber)
