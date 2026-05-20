# Linode Joomla Deployment One-Click App

Joomla is a free and open-source content management system (CMS) for publishing web content. This Marketplace App deploys Joomla 5.x on Ubuntu 24.04 with Apache, PHP 8.3, and MariaDB.

## Software Included

| Software  | Version | Description |
| :---      | :----   | :---        |
| Joomla    | 5.4.5   | Content management system (CMS) |
| MariaDB   | 10.11   | Relational database management system |
| PHP       | 8.3     | General-purpose scripting language |
| Apache    | 2.4     | Web server |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Sudo User | Creates limited `sudo` user with variable supplied username | Creates limited user from UDF supplied `username`. Note that usernames containing illegal characters will cause the play to fail. |
| SSH Key | Writes SSH pubkey to `sudo` user's `authorized_keys` | Writes UDF supplied `pubkey` to `/home/$username/.ssh/authorized_keys`. To add an SSH key to `root` please use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Secure SSH | Performs standard SSH hardening | The Secure SSH module writes to `/etc/ssh/sshd_config` to prevent password authentication and enable public key authentication for all users, including root. |
| Update Packages | Performs standard apt updates and upgrades | The Update Packages module performs apt update and upgrade actions as root. |
| UFW | Add UFW firewalls to the Linode | The UFW module will import a `ufw_rules.yml` provided in `roles/common/tasks` and enables the service. |
| Fail2Ban | Installs, activates and enables Fail2Ban | The Fail2Ban module installs, activates and enables the Fail2Ban service. |
| Secure MySQL | Generates the MariaDB root password, sets it, and removes anonymous users + test database. |
| Certbot SSL | The Certbot SSL module handles SSL/TLS certificate installation via Let's Encrypt, supporting Nginx certificate issuance. |
| Addons      | Optional monitoring/observability exporters (`newrelic`, `node_exporter`, `mysqld_exporter`, `opentelemetry_collector`, `alloy`). |

## Post-Deployment

When the playbook finishes, the operator can:

- Browse the public site at `https://<domain-or-rdns>/`.
- Log in to the admin dashboard at `https://<domain-or-rdns>/administrator/`.
- Read the generated credentials from `/home/<sudo_user>/.credentials`. The file contains:
  - Sudo username + password
  - MariaDB root password
  - Joomla DB name + user + password
  - Joomla admin username + password + email
  - Site URL + admin URL

The deployment installs Joomla's default `Cassiopeia` (frontend) and `Atum` (backend) templates — the operator picks/customizes their own theme post-deploy from `System → Templates`.

## Use our API

Customers can deploy Joomla through the Linode Marketplace or directly using the API. Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/), and substitute your own values for the defaults.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-2",
    "label": "joomla-occ-us-southeast",
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
        "site_name": "My Joomla Site",
        "admin_email": "admin@domain.tld",
        "joomla_admin_fullname": "Site Administrator",
        "joomla_db_user": "joomla",
        "joomla_db_name": "joomla_db",
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
  --label joomla-occ-us-southeast \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"soa_email_address":"email@domain.tld","site_name":"My Joomla Site","admin_email":"admin@domain.tld","joomla_admin_fullname":"Site Administrator","joomla_db_user":"joomla","joomla_db_name":"joomla_db","user_name":"sudo_user","disable_root":"No","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld","add_ons":"none"}'
```

## Resources

- [Deploy Joomla on Akamai Compute](https://www.linode.com/docs/marketplace-docs/guides/joomla/)
- [Joomla Programmers Documentation](https://manual.joomla.org/)
- [Joomla User Documentation](https://guide.joomla.org/)
