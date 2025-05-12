# Linode NetFoundry Edge Router Deployment One-Click APP

NetFoundry Edge Router provides ingress & egress in & out of a NetFoundry openziti network overlay.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| edge-router-registration | latest |  NetFoundry Edge Router Registration Script |
| edge-router-upgrade | latest | Nefoundry Edge Router Upgrade Script |
| edge-router-support bundle | latest | NetFoundry Edge Router Support Bundle Script |
| edge-router-nfhelp | latest | NetFoundry Edge Router help menu Script |
| saltstack-minion | 3006.* | SaltStack Minion Handles updates |
| openziti | latest | Openziti Software is downloaded with registration script |
| saltstack minion | 3006.* | SaltStack Minion Handles updates |


**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/$APP/tasks` and enables the service.  |


## Use our API

Customers can choose to the deploy the NetFoundry Edge Router server through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment, and substitute for default values.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "region": "us-southeast",
    "type": "g6-standard-1",
    "label": "netfoundry-edge-router-us-southeast",
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
        "registration_key": "XXXXXXXX",
        "user_name": "sudo_user",
        "password": "sudo_user_password",
        "pubkey": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
    }
}' https://api.linode.com/v4/linode/instances
```
CLI:
```
linode-cli linodes create \
  --image 'linode/ubuntu24.04' \
  --region us-southeast \
  --type g6-standard-1 \
  --label netfoundry-edge-router-us-southeast \
  --root_pass A_Really_Great_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"disable_root": "No","registration_key":"XXXXXXXX","user_name":"sudo_user","password":"sudo_user_password","pubkey":"ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"}'
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)

