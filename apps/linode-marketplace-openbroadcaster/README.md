# Linode OpenBroadcaster One-Click App

Deploy OpenBroadcaster Server (OBServer), open source radio and TV automation. Stations manage their media library, playlists and schedules in its web interface, and OpenBroadcaster players connect to it for playout. The server runs behind nginx with a Let's Encrypt certificate and redirects HTTP on port 80 to HTTPS.

The deployment sets a generated password for OpenBroadcaster's `admin` account and runs OpenBroadcaster's own install check before it finishes.

## Software Included

| Software        | Version        | Description                                              |
| :---            | :----          | :---                                                     |
| OpenBroadcaster | 5.4.0-20261107 | Radio and TV automation server with a web interface and API |
| nginx           | 1.24.0         | Web server                                               |
| PHP             | 8.3            | Runs OpenBroadcaster through its own PHP-FPM pool        |
| MariaDB         | 10.11          | Relational database                                      |
| FFmpeg          | 6.1.1          | Audio and video processing for media                     |
| Node.js         | 18.19.1        | Builds OpenBroadcaster's web interface                   |
| Composer        | 2.7.1          | PHP dependency manager                                   |
| Certbot         | 2.9.0          | Let's Encrypt certificate issuance and renewal           |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

| Item                       | Location                                         |
| :---                       | :---                                             |
| OpenBroadcaster code       | `/home/openbroadcaster/www`                      |
| OpenBroadcaster settings   | `/home/openbroadcaster/www/config.php`           |
| Media, thumbnails, uploads | `/home/openbroadcaster/files/`                   |
| Background tasks           | `ob.service` (`journalctl -u ob`)                |
| PHP-FPM pool               | `/etc/php/8.3/fpm/pool.d/openbroadcaster.conf`   |
| nginx site                 | `/etc/nginx/sites-available/<your-domain>`       |
| Credentials                | `/home/$USERNAME/.credentials`                   |

## Using OpenBroadcaster

Go to `https://<your-domain>/` and log in as `admin` with the OpenBroadcaster admin password from `/home/$USERNAME/.credentials`.

PHP-FPM and the background service run as the `openbroadcaster` user. Run OpenBroadcaster's command line tool as that user too:

```
sudo -u openbroadcaster /home/openbroadcaster/www/tools/cli/ob check install
```

No mail server is installed. To send password reset email, set `OB_EMAIL_HOST`, `OB_EMAIL_USER`, `OB_EMAIL_PASS`, `OB_EMAIL_TYPE` and `OB_EMAIL_PORT` for your SMTP provider in `config.php`. The file is readable only by the `openbroadcaster` user, so edit it with `sudo` and keep its owner and mode.

Node.js and npm stay installed because they build OpenBroadcaster's web interface, so it can be rebuilt after updating OpenBroadcaster.

## Linode Helpers Included

| Name              | Action |
| :---              | :---   |
| Hostname          | Sets the system hostname to the provided domain or the Linode's default rDNS. |
| Update Packages   | Performs apt update and upgrade actions as root. |
| UFW               | Enables UFW and allows ports 22, 80, and 443. |
| Fail2Ban          | Installs, activates and enables the Fail2Ban service. |
| Create DNS Record | Creates DNS records for the domain and subdomain using the Linode API. |
| Secure SSH        | Disables root login over SSH when requested, and password login too if an account SSH key was added. |
| SSH Key           | Deploys SSH keys for the sudo user. |
| Secure MySQL      | Sets a generated MariaDB root password and removes the anonymous users and the test database. |
| Certbot SSL       | Issues a Let's Encrypt certificate through the nginx plugin, which also redirects HTTP to HTTPS. |

## Resources

- [OpenBroadcaster](https://www.openbroadcaster.com/)
- [OpenBroadcaster documentation](https://support.openbroadcaster.com/)
- [OpenBroadcaster source code](https://github.com/openbroadcaster/observer)
