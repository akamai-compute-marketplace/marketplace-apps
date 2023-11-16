# Linode OpenVPN Deployment One-Click APP

OpenVPN is a widely trusted, free, and open-source VPN (virtual private network) application that creates encrypted tunnels for secure data transfer between computers that are not on the same local network.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Openvpn Access Server | latest |  Front-end GUI for OpenVPN |

**Supported Distributions:**

- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
|| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/$APP/tasks` and enables the service.  |


## Use our API

Customers can choose to the deploy the OpenVPN server through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment, and substitute for default values..

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu22.04",
    "region": "us-southeast",
    "type": "g6-standard-1",
    "label": "openvpn-oca-us-southeast",
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
        "user_name": "sudo_user",
        "password": "sudo_user_password",
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
  --stackscript_data '{"disable_root": "No","soa_email_address":"email@domain.tld","user_name":"sudo_user","password":"sudo_user_password","pubkey":"ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer","token_password":"A_Valid_API_Token","subdomain":"examplesubdomain","domain":"domain.tld"}'
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript referece](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)

