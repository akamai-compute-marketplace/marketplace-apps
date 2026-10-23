# Akamai Coolify Quick Deploy App

Coolify lets you run your own deployment platform on a single Linode. You can deploy apps, databases and ready-made services from a web dashboard, much like you would on Heroku or Vercel, but on a server you control.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Docker    | Latest    | Runs Coolify and everything you deploy with it. |
| Coolify   | Latest    | The dashboard and deployment engine. |
| Nginx     | Latest    | Sits in front of Coolify and handles HTTPS, including the live-update and terminal websockets. |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Works out the Linode's fully qualified domain name and adds it to `/etc/hosts`. |
| Update Packages   | Brings the system packages up to date before anything else is installed. |
| UFW   | Turns on the firewall and opens only the ports Coolify needs, listed in `roles/common/tasks/ufw_rules.yml`. |
| Fail2Ban   | Installs and starts Fail2Ban to block repeated failed logins. |

## Post-installation

### Access the dashboard

Open `https://<domain>` once the deployment finishes. The domain is the one you provided, or the Linode's default rDNS name (`<ip>.ip.linodeusercontent.com`). Sign in with the email you entered at deployment and the password stored in `/home/<user>/.credentials` on the Linode:

```
sudo cat /home/<user>/.credentials
```

### How the services are exposed

| Component | Listens on | Notes |
| :--- | :--- | :--- |
| Nginx | `0.0.0.0:80`, `0.0.0.0:443` | TLS termination with a Let's Encrypt certificate, config in `/etc/nginx/sites-available/<domain>`. |
| Coolify dashboard | `127.0.0.1:8000` | Proxied from `/`. |
| Coolify realtime (websocket) | `127.0.0.1:6001` | Proxied from `/app/`. |
| Coolify web terminal (websocket) | `127.0.0.1:6002` | Proxied from `/terminal/ws`. |

The three Coolify ports are bound to localhost by `/data/coolify/source/docker-compose.custom.yml`, so they are not reachable directly. Only ports 22, 80 and 443 are open in UFW.

### Verify the install

```
docker ps --format '{{.Names}}\t{{.Status}}'   # coolify, coolify-db and coolify-redis should be healthy
sudo ss -tlnp | grep -E ':(8000|6001|6002)'     # all bound to 127.0.0.1
sudo nginx -t && systemctl status nginx
sudo certbot certificates
```

In the dashboard, open **Servers > localhost > Validate Server**. It should report that the server is reachable and validated. This confirms the SSH key Coolify uses to manage its own host works.

### Test live updates and the web terminal

1. Open the browser developer tools, go to Network and filter by `WS`.
2. Reload the dashboard. A `wss://<domain>/app/...` connection should show status `101`.
3. Open **Servers > localhost > Terminal** and run a command. A `wss://<domain>/terminal/ws` connection should show status `101`.

If live updates or the terminal do not work, set the instance domain to `https://<domain>` under **Settings > Configuration**.

### Coolify's built-in proxy

Nginx owns ports 80 and 443, so Coolify's built-in Traefik proxy (`coolify-proxy`) cannot start. Set the proxy type to **None** under **Servers > localhost > Proxy**. Resources you deploy through Coolify must then be exposed with a port mapping and routed through nginx, or served from a separate server that runs its own proxy.

### File locations

| Path | Contents |
| :--- | :--- |
| `/data/coolify/source/.env` | Generated secrets and the root account settings. |
| `/data/coolify/source/docker-compose*.yml` | Coolify compose files, including the localhost port override. |
| `/data/coolify/ssh/keys/` | SSH key Coolify uses to reach the host. |
| `/data/coolify/{applications,databases,services,backups}` | Deployed resource data. |
| `/data/coolify/source/upgrade-*.log` | Upgrade logs. |

### Manage and upgrade

Coolify runs as the `coolify` systemd service (`/etc/systemd/system/coolify.service`), which brings up the compose stack in `/data/coolify/source` on every boot.

```
sudo systemctl status coolify
sudo systemctl restart coolify   # recreate the containers
docker logs -f coolify           # application logs
```

Upgrades are run from the dashboard under **Settings > Updates**. Do not edit `docker-compose.yml` or `docker-compose.prod.yml`, because they are overwritten on upgrade. Make changes in `docker-compose.custom.yml` instead.

### Notes

- Coolify manages the Linode over SSH as `root`. Selecting **Disable root access over SSH** during deployment will break the localhost server connection.
- Back up `/data/coolify/source/.env`. The `APP_KEY` in it is required to decrypt stored credentials.

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
      "label": "coolify",
      "type": "g6-standard-2",
      "region": "us-east"
    }' \
https://api.linode.com/v4/linode/instances
```

## Resources

- [Coolify documentation](https://coolify.io/docs)
