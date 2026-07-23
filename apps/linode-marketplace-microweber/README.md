# Microweber Quick Deploy App

[Microweber](https://microweber.com/) is a Drag-and-Drop website builder and a robust next-generation Content Management System (CMS) based on the PHP Laravel Framework. It empowers you to create various types of websites, online stores, and blogs without requiring any technical expertise.

At its core, Microweber is designed to support your journey toward online success. It offers an array of modules, customizations, and features tailored to e-commerce enthusiasts and bloggers. The CMS leverages the latest Drag & Drop technology and real-time text editing for an enhanced user experience, streamlined content management, visual appeal, and flexibility.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| Microweber | Latest | Drag-and-drop CMS and e-commerce website builder |
| Apache   | 2.4.58 | Web server |
| PHP      | 8.3.6  | Server-side scripting language |
| MariaDB  | 10.11.14 | Open-source relational database management system |

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

- Browse the site at `https://<domain-or-rdns>/` and log in to the admin panel at `https://<domain-or-rdns>/admin` (username `admin`, password from the credentials file). There is no setup wizard — the site is fully installed, and the installer endpoint (`/install`) returns 404.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - MariaDB root password
  - Microweber database name, user, and password
  - Microweber admin username, password, and email
- Start building: the deploy seeds default content on Microweber's stock template. Use Live Edit from the admin panel to compose pages, or set up the shop under Admin → Shop. Templates can be switched in Admin → Website → Design. See the [Microweber user guide](https://github.com/microweber/microweber-user-guide) and the [Microweber docs](https://github.com/microweber/microweber-docs) for more information on how to set up and use Microweber.

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
    "label": "microweber-server",
    "tags": [],
    "root_pass": "A_Secure_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 1051714,
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
  --label microweber-server \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 1051714 \
  --stackscript_data '{"soa_email_address":"email@domain.tld","admin_email":"admin@domain.tld","mw_db_user":"microweber","mw_db_name":"microweber","user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","add_ons":"none"}'
```

## Resources

- [Microweber user guide](https://github.com/microweber/microweber-user-guide)
- [Microweber docs](https://github.com/microweber/microweber-docs)
- [Microweber Repository](https://github.com/microweber/microweber)
