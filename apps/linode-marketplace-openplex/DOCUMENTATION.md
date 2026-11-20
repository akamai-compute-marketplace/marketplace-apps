---
title: "Deploy OpenPlex through the Linode Marketplace"
description: "Deploy OpenPlex, an open-source hosting control panel for websites, databases, e-mail, DNS and backups, on a Linode Compute Instance."
published: 2026-11-20
keywords: ['openplex','control panel','hosting panel','web hosting','wordpress','email','dns','docker']
tags: ["marketplace", "linode platform", "cloud manager"]
external_resources:
- '[OpenPlex documentation](https://openplex.dev)'
- '[OpenPlex on GitHub](https://github.com/avakiam/openplex)'
authors: ["Àlex Màrtir"]
contributors: ["Àlex Màrtir"]
license: '[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0)'
---

[OpenPlex](https://openplex.dev) is an open-source hosting control panel. It turns a single server into a complete web host, managed from a modern dashboard in English, Spanish or Catalan:

- **Websites:** PHP, Node.js, Python, Go or static sites, each in its own container, with free HTTPS certificates, staging copies and Git deploys.
- **One-click apps:** WordPress, Joomla and Drupal, installed, updated and hardened.
- **Databases:** MariaDB and PostgreSQL, with size limits and optional remote access.
- **E-mail:** mail domains, mailboxes and aliases with DKIM, and Roundcube webmail.
- **DNS, files and backups:** authoritative DNS, a web file manager and SFTP, and scheduled encrypted backups to S3-compatible storage such as Linode Object Storage.
- **Accounts:** customers and resellers with their own limits, API keys and a REST API, with modules for WHMCS and Blesta.

## Deploying a Marketplace App

{{% content "deploy-marketplace-apps-shortguide" %}}

{{% content "marketplace-verify-standard-shortguide" %}}

{{< note >}}
**Estimated deployment time:** OpenPlex should be fully installed within 5-10 minutes after the Compute Instance has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:** Ubuntu 24.04 LTS
- **Suggested plan:** a Shared CPU 4 GB plan or larger. 2 GB works for a few small websites without mail.

### OpenPlex Options

- **Email address** *(required)*: the contact address for the Let's Encrypt certificates of the panel and the websites.

{{% content "marketplace-required-limited-user-fields-shortguide" %}}

{{% content "marketplace-custom-domain-fields-shortguide" %}}

{{% content "marketplace-special-character-limitations-shortguide" %}}

## Getting Started after Deployment

### Accessing the OpenPlex control panel

1. Open a browser and go to the domain you entered when creating the instance, `https://panel.example.com`. Without a domain, use the instance's default rDNS name, `https://192-0-2-1.ip.linodeusercontent.com` (see [Managing IP Addresses](/docs/products/compute/compute-instances/guides/manage-ip-addresses/) to find it).

1. Sign in as `admin`. The password is in the credentials file of the limited sudo user. Log in to the instance over SSH (see [Connecting to a Remote Server Over SSH](/docs/guides/connect-to-server-over-ssh/)) and run:

    ```command
    sudo cat /home/$USER/.credentials
    ```

    ```output
    Sudo Username: user1
    Sudo Password: ...

    OpenPlex Panel: https://panel.example.com
    OpenPlex Username: admin
    OpenPlex Password: ...
    ```

    You can also print a one-time sign-in link for the admin account with `sudo openplexd login-link`.

1. After signing in, change the admin password and turn on two-factor authentication under your profile. The initial password file `/var/lib/openplex/initial-admin-password` is removed once the password is changed.

1. To host your first website, open **Websites**, choose **Add website** and enter its domain. Point the domain's A record at the instance's IP address and OpenPlex obtains its certificate automatically.

### Firewall

OpenPlex manages its own host firewall (nftables) and Fail2Ban, on the panel's **Firewall** page. SSH and SFTP (port 2222) are always open, HTTP/HTTPS are open for the panel and the websites, and the mail and DNS ports open only when those services are turned on. Don't enable UFW on the instance: it would block the ports OpenPlex opens.

### Sending e-mail

Linode restricts outbound SMTP (port 25) on new accounts. To send e-mail from the instance, [ask Linode support to lift the restriction](/docs/products/compute/compute-instances/guides/email/) and set the reverse DNS of the instance's IP address to your mail host name.

### Updates

The OpenPlex dashboard shows new releases and installs them (signed, with automatic rollback on failure). Ubuntu packages update through the usual `apt` tools.

{{% content "marketplace-update-note-shortguide" %}}
