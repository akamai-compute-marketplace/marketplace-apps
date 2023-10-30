# Linode Wordpress Deployment One-Click APP

WordPress is a popular dynamic content management system focused on blogs. WordPress can be deployed on a LAMP or LEMP stack, and features an extensive plugin framework and theme system that allows site owners and developers to use its simple, yet powerful publishing tools.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Wordpress | Latest    | Wordpress Content Management System |
| MariaDB   | 10.6      | Relational database |
| PHP       | 8.1       | General-purpose scripting language |
| Fail2ban  | 0.11.2    | Provides protection against brute force and authentication attempts |
| UFW       | 0.36      | Easy-to-use firewall wrapper used to allow HTTP/S and SSH ports |
| Certbot   | 1.12      | Is used to obtain HTTPS/TLS/SSL certificate for the provided domain |


**Supported Distributions:**

- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
|| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/$APP/tasks` and enables the service.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |
| Secure MySQL   | The Secure MySQL module will use `passgen.yml` to generate a secure root password and write to `group_vars/linode/vars`. It will then update MySQL to be accessible by local socket or root password, and remove anonymous users, test databases and remote access.  |

## Use our API

Customers can choose to the deploy the LAMP stack through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment, and substitute for default values..

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu22.04",
    "region": "us-southeast",
    "type": "g6-standard-1",
    "label": "wordpress-occ-us-southeast",
    "tags": [],
    "root_pass": "A_Really_Great_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 00000,
    "stackscript_data": {
        "disable_root": "No",
        "soa_email_address": "email@domain.tld",
        "webserver_stack": "LAMP",
        "site_title": "Example Site",
        "wp_admin_user": "admin",
        "wp_db_user": "wordpress",
        "wp_db_name": "wordpress",
        "user_name": "sudo_user",
        "password": "AReallyGreatPassword",
        "pubkey": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer",
        "token_password": "A_Valid_API_Token",
        "subdomain": "examplesubdomain",
        "domain": "domain.tld"
    }
}' https://api.linode.com/v4/linode/instances
```
CLI:
```
linode-cli linodes create \
  --image 'linode/ubuntu22.04' \
  --region us-southeast \
  --type g6-standard-1 \
  --label wordpress-occ-us-southeast \
  --root_pass A_Really_Great_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"disable_root": "No","soa_email_address":"email@domain.tld","webserver_stack":"LAMP","site_title":"Example Site","wp_admin_user":"ad,om","wp_db_user":"wordpress","wp_db_name":"wordpress","user_name":"sudo_user","password":"AReallyGreatPassword","pubkey":"ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld"}'
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)

