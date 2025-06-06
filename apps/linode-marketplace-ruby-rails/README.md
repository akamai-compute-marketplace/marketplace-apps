# Linode Ruby on Rails One-Click APP

Deploy a production-ready Ruby on Rails full-stack web framework that makes it easy to build modern web apps quickly and cleanly. It’s written in Ruby and follows the Model-View-Controller (MVC) pattern, which helps keep your code organized and easy to maintain. Rails built-in tools like routing, database migrations, and authentication so you can focus on building features instead of writing boilerplate.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Ruby      | 3.4.4     | Programming language |
| Rail      | 8.0.2     | Web application framework |
| Puma      |  6.6.0    | Ruby-based web server |
| Mise      | 2025.5.14 | Version manager for Ruby |
| Nginx     | 1.24.0    | Web server and reverse proxy |

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
| Certbot SSL | The Certbot SSL module handles SSL/TLS certificate installation via Let's Encrypt, supporting Nginx certificate issuance. |

## Use our API

Customers can choose to deploy Rails through the Akamai Compute Marketplace or directly using the API. Before using the commands below, you will need to create an [API token](https://techdocs.akamai.com/linode-api/reference/get-started) or configure [linode-cli](https://techdocs.akamai.com/cloud-computing/docs/getting-started-with-the-linode-cli) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN: Your Linode API token
- ROOT_PASS: Root password for the Linode
- USERNAME: System user that will be created
- SOA_EMAIL_ADDRESS: Email address for DNS records
- DOMAIN: Domain name (optional)
- SUBDOMAIN: Subdomain (optional)
- APP_NAME: Rails application name. This is used to create the app directory and service file

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="admin"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="www"
export APP_NAME="my-app"

curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "backups_enabled": true,
    "image": "linode/ubuntu24.04",
    "private_ip": true,
    "region": "us-southeast",
    "stackscript_data": {
        "user_name": "${USERNAME}",
        "disable_root": "No",
        "token_password": "${TOKEN}",
        "subdomain": "${SUBDOMAIN}",
        "domain": "${DOMAIN}",
        "soa_email_address": "${SOA_EMAIL_ADDRESS}",
        "app_name": "${APP_NAME}"
    },
    "stackscript_id": 609048,
    "type": "g6-dedicated-4",
    "label": "rails-example",
    "root_pass": "${ROOT_PASS}",
    "authorized_users": [
        "myuser"
    ],
    "disk_encryption": "disabled"
}' https://api.linode.com/v4/linode/instances
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="admin"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="www"
export APP_NAME="my-app"

linode-cli linodes create \
  --backups_enabled true \
  --image 'linode/ubuntu24.04' \
  --private_ip true \
  --region us-southeast \
  --stackscript_data '{"user_name": "${USERNAME}","disable_root":"No","token_password":"${TOKEN}","subdomain":"${SUBDOMAIN}","domain":"${DOMAIN}","soa_email_address":"${SOA_EMAIL_ADDRESS}","app_name":"${APP_NAME}"}' \
  --stackscript_id 609048 \
  --type g6-dedicated-4 \
  --label rails-example \
  --root_pass ${ROOT_PASS} \
  --authorized_users myuser \
  --disk_encryption disabled
```

## Resources

- [Create Linode via API](https://techdocs.akamai.com/linode-api/reference/post-linode-instance)
- [Stackscript reference](https://techdocs.akamai.com/cloud-computing/docs/write-a-custom-script-for-use-with-stackscripts#user-defined-fields-udfs)
- [Ruby Documentation](https://guides.rubyonrails.org/)