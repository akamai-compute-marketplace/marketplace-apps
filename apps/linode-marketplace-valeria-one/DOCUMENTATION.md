---
description: "Deploy Valeria One on a Linode Compute Instance. Valeria One is an open-source back office for small businesses that sell through WhatsApp, Instagram and Messenger."
keywords: ['crm','whatsapp','booking','small business','inbox']
tags: ["marketplace", "linode platform", "cloud manager"]
published: 2026-10-24
modified_by:
  name: Linode
title: "Deploy Valeria One through the Linode Marketplace"
external_resources:
- '[Valeria One](https://github.com/valeriaone/valeria-one)'
authors: ["Tadewan Pascua"]
---

[Valeria One](https://github.com/valeriaone/valeria-one) is an open-source (AGPL-3.0) back office for small businesses that sell through WhatsApp,
Instagram and Messenger: one inbox for every channel, customers, a pipeline, booking with no
double-booking, quotes with e-signature, payments to the business's own account, reminders and a simple
website, in 11 languages and with 14 countries' tax and privacy rules. It works without AI.

## Deploying a Marketplace App

{{< content "deploy-marketplace-apps-shortguide">}}

{{< content "marketplace-verify-standard-shortguide">}}

{{< note >}}
**Estimated deployment time:** Valeria One should be fully installed within 10 minutes after the Linode has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:** Ubuntu 24.04 LTS
- **Suggested plan:** Shared CPU, 2 GB (Linode 2 GB) or larger.

### Valeria One Options

{{< content "marketplace-required-limited-user-fields-shortguide">}}

{{< content "marketplace-custom-domain-fields-shortguide">}}

- **Email address** *(required)*: used for the Let's Encrypt certificate and the DNS records.

Without a domain, the app is served at the instance's own rDNS name
(`203-0-113-10.ip.linodeusercontent.com`) with an HTTPS certificate.

## Getting Started after Deployment

### Create the first account

1. Log in to the instance over SSH as your limited sudo user. The message of the day shows the app URL.
2. Open the credentials file: `cat /home/$USERNAME/.credentials`. It holds the sudo password and a
   **one-time setup link**. Lost it? Run `sudo valeria-one setup-link`.
3. Open the setup link in your browser and create the first account: business name, country (it sets the
   currency, tax, phone format and messaging and privacy rules), email and password. This account runs
   the server. Other people join by invitation (sign-ups are closed by default).

### Start using it

- **Start** walks you through switching on what you use (booking, payments, quotes, follow-ups, website…)
  and naming things in your own words.
- **Channels** connects WhatsApp, Messenger, Instagram, Telegram (paste a bot token), SMS, email or any
  system through a signed webhook.
- **Server** (for the first account) shows the version, backups, updates and background jobs.

### Everyday commands

```command
sudo valeria-one status     # what is running, version, last backup
sudo valeria-one backup     # back up now (data + this server's keys)
sudo valeria-one update     # newest release; rolls back by itself if it fails
sudo valeria-one help
```

Backups run every night and before every update, in `/opt/valeria-one/backups`. Keep copies off the
server: a backup holds the data and the server's keys.

### Credentials

The credentials file is at `/home/$USERNAME/.credentials`. Valeria One's own secret key and database
password are generated on the instance at install time and kept in `/opt/valeria-one/app/.env`
(readable by root only).

## Support

Valeria One is built and supported by its creator, Tadewan Pascua: tad.pascua@valai.mx ·
https://github.com/valeriaone/valeria-one/issues
