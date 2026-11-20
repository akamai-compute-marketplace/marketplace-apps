# Akamai OpenPlex Quick Deploy App

OpenPlex is an open-source hosting control panel. It turns a Linode into a complete web host — websites, databases, e-mail, DNS, files and backups — managed from a modern dashboard in English, Spanish or Catalan. Every website runs in its own container with a free HTTPS certificate.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| OpenPlex  | 0.33.0    | The control panel (`openplexd`), installed from its signed release. It updates itself from the dashboard. |
| Docker Engine | Latest | Runs the websites, databases, mail server and the edge proxy, from Docker's official repository. |
| Caddy     | Bundled   | The edge proxy in front of the panel and every website; gets the Let's Encrypt certificates. |
| nftables  | Ubuntu    | The host firewall, managed by OpenPlex. |
| Fail2Ban  | Ubuntu    | Blocks repeated failed SSH and panel logins. |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Works out the Linode's fully qualified domain name and sets it as the host name. |
| Update Packages   | Brings the system packages up to date before anything else is installed. |
| Create DNS Record | With an API token and a domain, creates the domain's zone and the A record in Linode DNS. |
| SSH Key / Secure SSH | Copies the account's SSH keys to the sudo user and, if requested, disables root login over SSH. |

UFW and the Fail2Ban helper are not used: the OpenPlex installer sets up its own nftables firewall (`table inet openplex`) and Fail2Ban, which the panel manages on its **Firewall** page. SSH (22) and SFTP (2222) are always open; HTTP/HTTPS (80, 443) are open for the panel and the websites; mail (25, 465, 587, 143, 993, 110, 995, 4190) and DNS (53) only when those services are turned on; everything else is closed.

## Post-installation

### Sign in to the panel

Open `https://<domain>` once the deployment finishes. The domain is the one you provided, or the Linode's default rDNS name (`<ip>.ip.linodeusercontent.com`). Sign in as `admin` with the password stored in `/home/<user>/.credentials` on the Linode, and change it under your profile:

```
sudo cat /home/<user>/.credentials
```

A one-time sign-in link for the admin account is also available at any time:

```
sudo openplexd login-link
```

### Change the panel's domain

The panel's address is `OPENPLEX_PANEL_DOMAIN` in `/etc/openplex/openplex.env`. Point the new name's A record at the Linode, change the value and restart OpenPlex; it gets the certificate on its own:

```
sudo nano /etc/openplex/openplex.env
sudo systemctl restart openplexd
```

### Verify the install

```
systemctl status openplexd
curl -fsS http://127.0.0.1:7080/api/v1/system/health
docker ps --format '{{.Names}}\t{{.Status}}'   # openplex-edge and the service containers
sudo nft list table inet openplex
```

### File locations

| Path | Contents |
| :--- | :--- |
| `/etc/openplex/openplex.env` | Settings: panel domain, ACME e-mail, listen address. |
| `/var/lib/openplex/openplex.db` | The panel database (SQLite). |
| `/var/lib/openplex/secret.key` | The key that encrypts stored secrets. Back it up. |
| `/var/lib/openplex/initial-admin-password` | The first admin password; removed once you change it. |
| `/var/lib/openplex/sites/<domain>/` | Website files and logs. |

### Notes

- Linode restricts outbound SMTP (port 25) on new accounts. To send e-mail from the Linode, ask Linode support to lift it, and set the reverse DNS (PTR) of the Linode's IP to the mail host name.
- Updates: the dashboard shows new OpenPlex releases and installs them (signed, with automatic rollback).
- Backups: set up scheduled, encrypted backups to S3-compatible storage (Linode Object Storage works) under **Backups**.

## Use our API

Make sure that the following values are updated at the top of the code block before running the commands:
- TOKEN
- ROOT_PASS

```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"
export SOA_EMAIL_ADDRESS="user@domain.tld"

curl -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X POST -d '{
      "image": "linode/ubuntu24.04",
      "root_pass": "${ROOT_PASS}",
      "stackscript_id": 0,
      "stackscript_data": {
        "soa_email_address": "${SOA_EMAIL_ADDRESS}",
        "user_name" : "${USERNAME}"
      },
      "booted": true,
      "label": "openplex",
      "type": "g6-standard-2",
      "region": "us-east"
    }' \
https://api.linode.com/v4/linode/instances
```

## Resources

- [OpenPlex documentation](https://openplex.dev)
- [Source code and issues](https://github.com/avakiam/openplex)
