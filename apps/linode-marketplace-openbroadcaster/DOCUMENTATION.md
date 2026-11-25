---
description: "Deploy OpenBroadcaster on a Linode Compute Instance. OpenBroadcaster is open source radio and TV automation: a web application where a station manages its media library, playlists and schedules, which OpenBroadcaster players play out."

keywords: ['radio automation','broadcast','playout','media management']
tags: ["marketplace", "linode platform", "cloud manager"]
published:
modified_by:
  name: Linode
title: "Deploy OpenBroadcaster through the Linode Marketplace"
external_resources:
- '[OpenBroadcaster](https://www.openbroadcaster.com/)'
authors: ["Linode"]
---

[OpenBroadcaster](https://www.openbroadcaster.com/) is open source radio and TV automation. OpenBroadcaster Server (OBServer) is the web application where a station manages its media library, playlists and schedules. One server can drive one or many OpenBroadcaster players in sync, and its documented API lets stations share media and metadata with revocable keys.

## Deploying a Marketplace App

{{< content "deploy-marketplace-apps-shortguide">}}

{{< content "marketplace-verify-standard-shortguide">}}

{{< note >}}
**Estimated deployment time:** OpenBroadcaster should be fully installed within 15 minutes after the Compute Instance has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:** Ubuntu 24.04 LTS
- **Recommended plan:** All plan types and sizes can be used. Media is stored on the Compute Instance's disk, so choose a plan with enough storage for your library.

### OpenBroadcaster Options

- **Email address** *(required)*: Used for the Let's Encrypt SSL certificate and as the email address of the OpenBroadcaster `admin` account.

{{< content "marketplace-required-limited-user-fields-shortguide">}}

The limited sudo user can't be named `openbroadcaster`, which is reserved for the user that runs OpenBroadcaster.

Selecting **Yes** for **Disable root access over SSH** and adding an account SSH key is recommended: the deployment then turns off root login and password login over SSH. With **No**, both stay enabled.

{{< content "marketplace-custom-domain-fields-shortguide">}}

{{< content "marketplace-special-character-limitations-shortguide">}}

## Getting Started after Deployment

### Accessing OpenBroadcaster

Open your web browser and go to the custom domain you entered during deployment, or the rDNS domain of your Compute Instance (e.g., `192-0-2-1.ip.linodeusercontent.com`). Log in as `admin` with the OpenBroadcaster admin password from the credentials file described below.

![The OpenBroadcaster login page](openbroadcaster-login.png)

After logging in, the dashboard opens. From here you manage media, playlists, schedules and users.

![The OpenBroadcaster dashboard](openbroadcaster-dashboard.png)

New user registration is on by default, so the login page shows **Create New Account**. To turn off public sign-ups, go to **admin** > **User Management** and clear **Allow new user registration from the welcome screen**. The change saves right away.

### Obtaining the Credentials

The passwords are generated during the deployment and saved in the home directory of the limited sudo user. Log in to your Compute Instance through the [LISH Console](https://www.linode.com/docs/products/compute/compute-instances/guides/lish/#through-the-cloud-manager-weblish) or over SSH as that user, then read the file:

```
cat ~/.credentials
```

It contains:

- the sudo user's name and password;
- the MariaDB root password;
- the OpenBroadcaster database name, user and password;
- the OpenBroadcaster URL;
- the OpenBroadcaster admin user and password.

### Where OpenBroadcaster Lives

| Item                       | Location                                       |
| :---                       | :---                                           |
| OpenBroadcaster code       | `/home/openbroadcaster/www`                    |
| OpenBroadcaster settings   | `/home/openbroadcaster/www/config.php`         |
| Media, thumbnails, uploads | `/home/openbroadcaster/files/`                 |
| Background tasks           | `ob.service` (`journalctl -u ob`)              |

PHP-FPM and the background service run as the `openbroadcaster` user. Run OpenBroadcaster's command line tool as that user too, for example to check the installation:

```
sudo -u openbroadcaster /home/openbroadcaster/www/tools/cli/ob check install
```

### Sending Email

No mail server is installed, so OpenBroadcaster can't send password reset email until you add an SMTP provider. Set `OB_EMAIL_HOST`, `OB_EMAIL_USER`, `OB_EMAIL_PASS`, `OB_EMAIL_TYPE` and `OB_EMAIL_PORT` in `config.php`. OpenBroadcaster uses SMTP only when all five are set. The file is readable only by the `openbroadcaster` user, so edit it with `sudo` and keep its owner and mode.

### More Information

You may wish to consult the following resources for additional information on this topic. While these are provided in the hope that they will be useful, please note that we cannot vouch for the accuracy or timeliness of externally hosted materials.

- [OpenBroadcaster](https://www.openbroadcaster.com/)

- [Help and support](https://www.openbroadcaster.com/resource/help-and-support/)

- [Documentation](https://support.openbroadcaster.com/)

- [Source code](https://github.com/openbroadcaster/observer)

{{< content "marketplace-update-note-shortguide">}}
