# Linode OpenLiteSpeed Wordpress Deployment One-Click APP

OpenLiteSpeed is a high-performance, lightweight, open-source HTTP server that helps your site load faster than ever. The OpenLiteSpeed Wordpress One-Click app automatically installs OpenLiteSpeed, PHP, MySQL Server, WordPress, LiteSpeed Cache, and other useful applications. OpenLiteSpeed features HTTP/3 support and easy setup for SSL.

## Software Included

| Software        | Version | Description   |
| :---            | :----   | :---          |
| OpenLiteSpeed   | 1.7     | High-performance, lightweight, open-source HTTP server |
| Wordpress       | Latest  | Open-source content management system |
| LiteSpeed PHP   | 8.1     | LiteSpeed Web Server is a high-performance, high-scalability web server that is known for its speed and efficiency |
| MariaDB         | 10.11  | Open-source relational database management system |

**Supported Distributions:**

- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/$APP/tasks` and enables the service.  |
| Secure MySQL   | The Secure MySQL module will use `passgen.yml` to generate a secure root password and write to `group_vars/linode/vars`. It will then update MySQL to be accessible by local socket or root password, and remove anonymous users, test databases and remote access.  |

## How to Access the Installed Software

See the Linode tab at: https://docs.litespeedtech.com/cloud/images/wordpress/

## Use our API

Customers can choose to the deploy the openlitespeed app through the Akamai Compute Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN
- ROOT_PASS

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export SOA_EMAIL_ADDRESS="email@domain.com"

curl -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X POST -d '{
      "backups_enabled": true,
      "swap_size": 512,
      "image": "linode/ubuntu2204",
      "root_pass": "${ROOT_PASS}",
      "stackscript_id": 00000000000,
      "stackscript_data": {
        "disable_root": "${disable_root}",
        "user_name": "${user_name}",
        "site_title": "${site_title}",
        "wp_admin_user": "${wp_admin_user}",
        "wp_db_user": "${wp_db_user}",
        "wp_db_name": "${wp_db_name}",
        "soa_email_address": "${SOA_EMAIL_ADDRESS}"
      },
      "authorized_users": [
        "myUser",
        "secondaryUser"
      ],
      "booted": true,
      "label": "linode123",
      "type": "g6-standard-2",
      "region": "us-east",
      "group": "Linode-Group"
    }' \
https://api.linode.com/v4/linode/instances
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export SOA_EMAIL_ADDRESS="email@domain.com"

linode-cli linodes create \
  --label linode123 \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 00000000000 \
  --stackscript_data '{"disable_root": "${disable_root}", "user_name": "${user_name}", "site_title": "${site_title}", "wp_admin_user": "${wp_admin_user}", "wp_db_user": "${wp_db_user}", "wp_db_name": "${wp_db_name}", "soa_email_address": "${SOA_EMAIL_ADDRESS}"}' \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
  --authorized_users "myUser"
  --authorized_users "secondaryUser"
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
