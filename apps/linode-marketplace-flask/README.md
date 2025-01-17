# Linode Flask Deployment One-Click APP

The Linode Marketplace One-Click App for Flask provides everything you need to get started with hosting web applications using Python. This stack includes Flask (a lightweight WSGI web application framework), Nginx as a reverse proxy, and Gunicorn as the WSGI HTTP server. After deployment, you can modify the sample Flask application or upload your own Flask application code to start building your web project.

* The sample project can be found in /var/www/flask_project
* The Gunicorn systemd service can be found in /etc/systemd/system/gunicorn.service
* The Gunicorn socket is located at /tmp/gunicorn.sock

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Python    | 3.x       | Programming language used for Flask applications |
| Flask     | Latest    | Lightweight WSGI web application framework |
| Nginx     | Latest    | Web server used as reverse proxy |
| Gunicorn  | Latest    | Python WSGI HTTP Server |
| Fail2ban  | Latest    | Provides protection against brute force and authentication attempts |
| UFW       | Latest    | Easy-to-use firewall wrapper used to allow HTTP/S and SSH ports |
| Certbot   | Latest    | Used to obtain HTTPS/TLS/SSL certificates for the provided domain |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Sets up the system hostname based on domain information. Uses the provided domain/subdomain or falls back to the Linode's default rDNS. |
| Update Packages   | Performs system package updates and upgrades using apt. |
| UFW   | Configures and enables UFW firewall with standard ports (SSH, HTTP, HTTPS). Additional ports can be configured in the application's UFW rules. |
| Fail2Ban   | Installs and configures Fail2Ban for protection against brute force attempts. |
| SSL/TLS   | Configures SSL certificates via Certbot. Uses the provided domain/subdomain or falls back to the Linode's default rDNS. |


## Use our API

You can deploy the Flask stack through the Linode Marketplace or directly using the API/CLI. Before using the commands below, you'll need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/).

Update these values before running the commands:
- TOKEN
- SOA_EMAIL_ADDRESS
- ROOT_PASS
- DOMAIN (optional)

SHELL:
```
export TOKEN="YOUR API TOKEN"
export SOA_EMAIL_ADDRESS="user@domain.tld"
export ROOT_PASS="aComplexP@ssword"

curl -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X POST -d '{
      "backups_enabled": true,
      "swap_size": 512,
      "image": "linode/ubuntu2204",
      "root_pass": "${ROOT_PASS}",
      "stackscript_id": 00000000000,
      "stackscript_data": {
        "soa_email_address": "${SOA_EMAIL_ADDRESS}",
        "domain": "${DOMAIN}"
      },
      "authorized_users": [
        "myUser",
        "secondaryUser"
      ],
      "booted": true,
      "label": "flask-app",
      "type": "g6-standard-2",
      "region": "us-east",
      "group": "Linode-Group",
      "authorized_keys": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer",
      "disk_encryption": "disabled"
    }' \
https://api.linode.com/v4/linode/instances
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export SOA_EMAIL_ADDRESS="user@domain.tld"
export ROOT_PASS="aComplexP@ssword"

linode-cli linodes create \
  --label flask-app \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 00000000000 \
  --stackscript_data '{"soa_email_address": "${SOA_EMAIL_ADDRESS}", "domain": "${DOMAIN}"}' \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
  --authorized_users "myUser"
  --authorized_users "secondaryUser"
  --disk_encryption disabled
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Linode Flask Guide](https://www.linode.com/docs/marketplace-docs/guides/flask/)

