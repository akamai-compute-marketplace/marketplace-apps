# Linode LiveSwitch Deployment One-Click APP

The Linode Marketplace One-Click App for LiveSwitch provides everything you need to get started with hosting real-time communication applications. This stack includes LiveSwitch (a real-time communications platform), Docker, and everything needed to run LiveSwitch in Docker containers. After deployment, you can access the LiveSwitch admin console and start building your own real-time communication applications.

* The Docker Compose files can be found in /home/$USER/liveswitch-secure/
* The NGINX configuration for LiveSwitch can be found in /etc/nginx/sites-available/domain.tld
* LiveSwitch is accessible via HTTPS on your domain

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Docker    | Latest    | Platform for running the LiveSwitch containers |
| Docker Compose | Latest | Tool for defining and running multi-container Docker applications |
| LiveSwitch Gateway | Latest | Main LiveSwitch service for WebRTC communication |
| Redis     | Latest    | In-memory data structure store for signaling and messaging |
| PostgreSQL | Latest   | Database for LiveSwitch configuration and data |
| RabbitMQ  | Latest    | Message broker for recording workflows |
| Nginx     | Latest    | Web server used as reverse proxy |
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

You can deploy the LiveSwitch stack through the Linode Marketplace or directly using the API/CLI. Before using the commands below, you'll need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/).

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
      "label": "liveswitch-app",
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
  --label liveswitch-app \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 00000000000 \
  --stackscript_data '{"soa_email_address": "${SOA_EMAIL_ADDRESS}", "domain": "${DOMAIN}"}' \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer" \
  --authorized_users "myUser" \
  --authorized_users "secondaryUser" \
  --disk_encryption disabled
```

## Resources

- [Linode LiveSwitch Guide](https://www.linode.com/docs/marketplace-docs/guides/liveswitch/)
- [LiveSwitch Documentation](https://developer.liveswitch.io/)
- [Docker Documentation](https://docs.docker.com/)

