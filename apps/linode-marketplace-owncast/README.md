# Linode Owncast Deployment One-Click APP

Owncast is a free and open-source live streaming and chat server. It allows you to run your own live streaming platform, giving you complete control and ownership over your content and user experience.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| NGINX     | Latest    | Web server and reverse proxy |
| FFmpeg    | Latest    | Multimedia framework for handling video streams |
| Owncast   | 0.2.1     | Self-hosted live streaming and chat platform |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | The UFW module will utilize a list generated by `linode_helpers/ufw/ufwgen.yml` in the `group_vars/linode/vars` and enables the service.  |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |
| Create DNS Record | The Create DNS Record module creates DNS records for domains and subdomains using the Linode API, including validation of DNS propagation. |
| Secure SSH | The Secure SSH module configures SSH security settings including disabling root login and password authentication when appropriate. |
| SSH Key | The SSH Key module manages SSH key deployment for the sudo user, supporting both custom public keys and account keys. |
| Certbot SSL | The Certbot SSL module handles SSL/TLS certificate installation via Let's Encrypt, supporting Apache, Nginx, and standalone certificate issuance. |

## Use our API

Customers can choose to deploy the Owncast app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN - Your Linode API token
- ROOT_PASS - Root password for the Linode
- USERNAME - System user that will be created
- SOA_EMAIL_ADDRESS - Email address for DNS records
- DOMAIN - Domain name (optional)
- SUBDOMAIN - Subdomain (optional)

```
SHELL:
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="stream"

curl -H "Content-Type: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
-X POST -d '{
"authorized_users": [
"user1",
"user2"
],
"backups_enabled": true,
"booted": true,
"image": "linode/ubuntu24.04",
"label": "owncast-server",
"private_ip": true,
"region": "us-southeast",
"root_pass": "${ROOT_PASS}",
"stackscript_data": {
"user_name": "${USERNAME}",
"disable_root": "Yes",
"token_password": "${TOKEN}",
"subdomain": "${SUBDOMAIN}",
"domain": "${DOMAIN}",
"soa_email_address": "${SOA_EMAIL_ADDRESS}"
},
"stackscript_id": 00000000000,
"type": "g6-nanode-1",
"tags": ["mytag"],
"disk_encryption": "disabled"
}' https://api.linode.com/v4/linode/instances

CLI:
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="stream"

linode-cli linodes create \
--image 'linode/ubuntu24.04' \
--private_ip true \
--label owncast-server \
--root_pass ${ROOT_PASS} \
--booted true \
--stackscript_id 00000000000 \
--stackscript_data '{"user_name": "${USERNAME}","disable_root":"Yes","token_password":"","subdomain":"${SUBDOMAIN}","domain":"${DOMAIN}","soa_email_address":"${SOA_EMAIL_ADDRESS}"}' \
--region us-east \
--type g6-nanode-1 \
--tags mytag \
--authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
--authorized_users "user1"
--authorized_users "user2"
--disk_encryption disabled
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript reference](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
- [Owncast Documentation](https://owncast.online/docs/)
- [Owncast Configuration](https://owncast.online/docs/configuration/)