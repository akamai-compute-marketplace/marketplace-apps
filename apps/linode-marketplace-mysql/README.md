# Linode MySQL/MariaDB Deployment One-Click APP

MySQL and MariaDB are an open-source database management systems that uses a relational database and SQL (Structured Query Language) to manage their data. This One-Click app allows the user to select which fork to install, MySQL-Server or MariaDB-Server

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| MySQL-Server    | latest / 8.0    | database |
| MariaDB-Server | latest / 10.5 | database |


**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | The UFW module will utilize a list generated by `linode_helpers/ufw/ufwgen.yml` in the `group_vars/linode/vars` and enables the service.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |

## Use our API

Customers can choose to the deploy the MySQL/MariaDB app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN
- ROOT_PASS

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"

curl -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X POST -d '{
      "backups_enabled": true,
      "swap_size": 512,
      "image": "linode/ubuntu2404",
      "root_pass": "${ROOT_PASS}",
      "stackscript_id": 607026,
      "stackscript_data": {
        "username": "${USERNAME}",
        "sql_db": "mariadb"
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
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"

linode-cli linodes create \
  --label linode123 \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 607026 \
  --stackscript_data "username": "${USERNAME}", "sql_db": "mariadb" \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
  --authorized_users "myUser"
  --authorized_users "secondaryUser"
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)

