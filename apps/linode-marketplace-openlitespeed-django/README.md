# Linode OpenLiteSpeed Deployment One-Click APP

OpenLiteSpeed is a high-performance, lightweight, open-source HTTP server that helps your site load faster than ever. The Django OpenLiteSpeed One-Click app automatically installs Linux, OpenLiteSpeed, Python LSAPI and ACME to deliver fast and scalable web applications. OpenLiteSpeed features HTTP/3 support, and easy setup for SSL and RewriteRules.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| OpenLiteSpeed    | 1.7    | High-performance, lightweight, open-source HTTP server |
| Django    | 5.0    | High-level Python web framework that encourages rapid development and clean, pragmatic design |


**Supported Distributions:**

- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |

## How to Access the Installed Software

See the Linode tab at: https://docs.litespeedtech.com/cloud/images/django/

## Use our API

Customers can choose to the deploy the openlitespeed app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

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
  --stackscript_data '{"soa_email_address": "${SOA_EMAIL_ADDRESS}"}' \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
  --authorized_users "myUser"
  --authorized_users "secondaryUser"
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
