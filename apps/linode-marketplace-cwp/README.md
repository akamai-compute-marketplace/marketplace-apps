# Linode Control Web Panel (CWP) Deployment One-Click APP

Control Web Panel (CWP) is a free, open-source Linux hosting control panel. It turns a single server into a complete hosting platform: web server with Nginx and Varnish caching, multiple PHP versions, mail (Postfix and Dovecot), DNS (BIND or PowerDNS), FTP, Let's Encrypt certificates, per-account backups, cPanel account migration and a REST API.

The app installs CWP unattended on AlmaLinux 9 and leaves the first-run wizard to the customer, so the server is ready to configure from the panel in a few minutes with no terminal work. No licence fee is charged for the panel at any scale.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Control Web Panel    | latest    | Hosting Control Panel |

**Supported Distributions:**

- AlmaLinux 9


## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| SSH Key   | The SSH Key module copies the root account's SSH public keys to the limited sudo user so it can log in with the same key. |
| Secure SSH   | The Secure SSH module hardens `sshd_config` when root login is disabled. |
| CILog   | The CILog module reports the deployment status to the Marketplace CI pipeline in staging mode. |

## Use our API

Customers can choose to the deploy Control Web Panel through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN

SHELL:
```bash
export TOKEN="YOUR API TOKEN HERE"

# List of Linodes you have access to
curl -H "Authorization: Bearer ${TOKEN}" \
  https://api.linode.com/v4/linode/instances
```

## Links

- [Control Web Panel documentation](https://control-webpanel.com/installation-instructions)
- [Control Web Panel support](https://support.centos-webpanel.com/)
