# Linode Zabbix Deployment One-Click APP

Zabbix is an enterprise-class, open-source, distributed monitoring solution. Designed as an all-in-one monitoring solution, Zabbix can track performance and availability of network servers, devices, services, and other IT resources. Zabbix empowers administrators to quickly respond to incidents with on-screen display capabilities and alerts by email, SMS, or Jabber. Users can also collect, store, manage, and analyze information received from IT infrastructure. Actively used by SMBs and large enterprises across all industries and in almost every country, Zabbix has a robust community driving its continued development.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Nginx    | latest   | Open Source Webserver |
| MariaDB | 10.6.16   | Open Source SQL Database |
| PHP-FPM | 8.1 | Server Side scripting |
| Zabbix | 6.0 | Open Source Monitoring |

**Supported Distributions:**

- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | The UFW module will utilize a list generated by `linode_helpers/ufw/ufwgen.yml` in the `group_vars/linode/vars` and enables the service.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |

## Use our API

Customers can choose to the deploy the Yacht app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN
- ROOT_PASS

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"

curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "authorized_users": [],
    "backups_enabled": false,
    "booted": true,
    "image": "linode/ubuntu22.04",
    "label": "zabbix-oca-us-mia",
    "private_ip": false,
    "region": "us-mia",
    "root_pass": "$ROOT_PASS",
    "stackscript_data": {
        "disable_root": "No",
        "user_name": "sudo_user",
        "soa_email_address": "email@tld.com",
        "token_password": "$TOKEN",
        "subdomain": "zabbix",
        "domain": "example.com"
    },
    "stackscript_id": 741208,
    "tags": [],
    "type": "g6-standard-4"
}' https://api.linode.com/v4/linode/instances
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
# add udfs

linode-cli linodes create \
  --label zabbix-oca-us-mia \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 741208 \
  --stackscript_data '{"disable_root": "No","user_name":"sudo_user","soa_email_address":"email@tld.com","token_password":"$TOKEN","subdomain":"zabbix","domain":"example.com"}' \
  --region us-mia \
  --type g6-standard-4 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer" \
  --authorized_users "myUser" \
  --authorized_users "secondaryUser"
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
